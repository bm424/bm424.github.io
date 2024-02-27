Title: Implementing Functional Graph Algorithms in Python (Part 3: Algorithms)
Date: 2023-01-02 00:00
---

_This article was originally published on
Medium ([link](https://medium.com/@benhmartineau/implementing-functional-graph-algorithms-in-python-part-3-algorithms-a305751f9d41))_

---

Welcome back to this series on functional programming in Python! We’ve been looking at how to implement [inductive
graphs](https://www.cambridge.org/core/journals/journal-of-functional-programming/article/inductive-graphs-and-functional-graph-algorithms/2210F7C31A34EA4CF5008ED9E7B4EF62) (
Erwig 2001) in Python. In the [first part](#2022-12-19-functional_graph_algorithms_1), we looked at how to implement the
necessary data types, and in the [second part](#2022-12-26-functional_graph_algorithms_2) we implemented some basic
functions.

In this section, I’ll show you how to implement topological sorting and Dijkstra’s algorithm for shortest paths using
the methods described in the paper. We’ll use new Python features like `match` statements to get very close to the
declarative Haskell description of these algorithms.

# Topological Sorting

A [topological sort](https://en.wikipedia.org/wiki/Topological_sorting) of a graph is a list of its nodes which are
followed in an order where “earlier” nodes come before "later" nodes (for a more precise definition see the linked
Wikipedia article). Strictly speaking, this is only possible if the graph is acyclic — this means there are no loops.
It’s useful for resolving the “order” that processes should be evaluated in if, for example, your graph represents data
flow. Topological sorts are not unique.

## Depth-First Forest

The paper describes an inductive graph algorithm for the topological sort which relies on a "depth-first forest" which
can be derived from the graph. What is this?

![A single graph with seven nodes, the first two labeled 'a' and 'b', with directed edges joining some of the other nodes. An arrow labeled 'dff' shows the transformation to the depth first forest. The forest shows the same seven nodes, but 'a' and 'b' now represent the roots of two separate subtrees.](depth_first_forest.png)

_An illustration of the operation of "depth first forest" on a graph._

We can decompose the graph into a number of “trees”. Trees are like graphs but nodes only ever have one predecessor.
Starting at any node, we can get a single tree by removing it and following successors until we run out of nodes. To get
the forest, we just need to start searching from all nodes. The algorithm described in Haskell notation looks like this:

```hs
df :: [Node] -> Graph a b -> ([Tree Node], Graph a b)
df [] g = ([], g)
df (v:vs) (c &v g) = (Br v f:f', g₂) where (f, g₁) = df (suc c) g; (f', g₂) = df vs g₁
df (v:vs) g = df vs g
```

## Implementation

Phew! That’s a confusing definition. Let’s break it down in Python. Firstly, the function says that given a queue of
nodes `[Node]` and a graph `Graph a b`, `df` returns a tuple (a Haskell-style tuple with a fixed length). The first
element of
the tuple is a queue of trees of nodes, and the second is a graph. Since we’re using methods to implement these
functions in Python, it’s almost the same:

```python
class Graph(abc.ABC, typing.Generic[A, B]):
    ...

    def _dff(self, nodes: tuple[Node, ...]) -> tuple[tuple[Tree[Node], ...], "Graph[A, B]"]:
        ...
```

The next line, `df [] g = ([], g)`, says that if there are no nodes, we just return an empty tuple and the graph itself:

```python
class Graph(abc.ABC, typing.Generic[A, B]):
    ...

    def _dff(self, nodes: tuple[Node, ...]) -> tuple[tuple[Tree[Node], ...], "Graph[A, B]"]:
        if not nodes:
            return (), self
        ...
```

The line after this, `df (v:vs) (c &v g) = (Br v f:f', g₂) where (f, g₁) = df (suc c) g; (f', g₂) = df vs g₁`, says: if
we
can find the first node, `v`, in the graph, then calculate the forest for all of the successors of that node in the
graph
_without_ that node. Then, carry on calculating trees with whatever nodes `vs` we haven’t yet looked at. We then
construct a
tree with the node at the head of the forest of successors, then return it alongside all the other trees we’ve found.

```python
class Graph(abc.ABC, typing.Generic[A, B]):
    ...

    def _dff(self, nodes: tuple[Node, ...]) -> tuple[tuple[Tree[Node], ...], "Graph[A, B]"]:
        ...
        head, *tail = nodes  # (v:vs)
        match self.pop(head):  # (c &v g)
            case c, g:
                f, g1 = g._dff(c.suc)  # (f, g1) = df (suc c) g
                f_, g2 = g1._dff(tuple(tail))  # (f', g2) = df vs g1
                return (Tree(head, f), *f_), g2  # (Br v f:f', g2)
```

Why have I used match-case here? Well, what happens if we can’t find the node `v` in the graph? We just carry on with
the
other nodes, as in the final line of the algorithm `df (v:vs) g = df vs g`:

```python
class Graph(abc.ABC, typing.Generic[A, B]):
    ...

    def _dff(self, nodes: tuple[Node, ...]) -> tuple[tuple[Tree[Node], ...], "Graph[A, B]"]:
        ...
        head, *tail = nodes  # (v:vs)
        match self.pop(head):  # (c &v g)
            case c, g:
                ...
            case None:
                return self._dff(tuple(tail))  # df vs g
```

So the match statement allows a nice clean syntax demonstrating both cases.

Finally, we can wrap the whole thing in a public `dff` method which just passes all of the graph’s nodes into the
function, so that we get back a forest that spans the whole graph:

```python
class Graph(abc.ABC, typing.Generic[A, B]):
    ...

    def _dff(self, nodes: tuple[Node, ...]) -> tuple[tuple[Tree[Node], ...], "Graph[A, B]"]
        ...

    def dff(self):
        return self._dff(self.nodes())[0]
```

The topological sort of the graph is derived from the depth-first spanning forest. We can walk through each tree from
the bottom up (using a function called `postOrder`). The reverse of this sequence is a topological sort!

```python
class Graph(abc.ABC, typing.Generic[A, B]):
    ...

    def _dff(self, nodes: tuple[Node, ...]) -> tuple[tuple[Tree[Node], ...], "Graph[A, B]"]
        ...

    def dff(self) -> tuple[Tree[Node], ...]:
        return self._dff(self.nodes())[0]

    def topsort(self) -> tuple[Node, ...]:
        return tuple(reversed(concat_map(Tree.post_order, self.dff())))
```

Isn't that sweet?

# Dijkstra's Shortest Path Algorithm

Finally, let’s implement the inductive graph version of Dijkstra’s shortest path algorithm. There’s a bit of underlying
machinery here involving what the paper calls `LRTrees` and `LPaths` which I won’t get in to here, but feel free to take
a
look at the code. The important thing for the implementation is that `LPaths` are labeled lists of nodes which can be
compared using `<` — i.e. one is “shorter” than another. This means they can be used in a heap.

## Definition

```hs
dijkstra :: Real b => Heap (LPath b) -> Graph a b -> LRTree b
```

This says that for a graph with node edges labeled with a real number, and a heap (a data structure where we can
efficiently get the smallest value) of paths, `dijkstra` will return a `LRTree` (a queue of labeled paths) representing
the shortest paths between a given node and all other reachable nodes.

```hs
dijkstra h g | isEmptyHeap h || isEmpty g = []
```

Simple enough: there are no short paths in an empty graph. For non-empty graphs, the heap should never be empty, because
we always have a zero-length path from a node to itself.

```hs
dijkstra (p@((v,d):_)≺h) (c &v g) = p:dijkstra (mergeAll h:expand d p c)) g
```

😱 What is this nightmare? In words, it says: if the first node `v` in the smallest path `p` in the heap can be found in
the graph, return that path and keep searching with `v` removed and a heap with that path removed and a set of new paths
starting at all the successors. What this means is that when a new, shorter path to a given node is found it replaces
the existing one.

Finally, if the shortest path’s first node `v` is not in the graph, we can just carry on with trying to find shorter
paths than the ones we’ve got:

```hs
dijkstra (_≺h) g = dijkstra h g
```

## Implementation

Like the topological sort, this algorithm maps very nicely to Python. I’ve included the _`expand` method for
completeness:

```python
class Graph(abc.ABC, typing.Generic[A, B]):
    ...

    @staticmethod
    def _expand(
            item: float, lpath: "LPath[float]", context: Context[A, float]
    ) -> tuple[ImmutableHeap["LPath[float]"], ...]:
        return tuple(
            ImmutableHeap.unit(LPath((LNode(node, item + label), *lpath)))
            for label, node in context.successors
        )

    def _dijkstra(self, heap: ImmutableHeap["LPath[float]"]) -> "LRTree[float]":
        if not heap or self.is_empty:  # isEmptyHeap h || isEmpty g
            return LRTree()
        p, h = heap.pop()  # p < h
        (v, d), *_ = p  # p@((v, d): _)
        match self.pop(v):  # c &v g
            case (c, g):
                return LRTree(
                    (p, *g._dijkstra(ImmutableHeap.merge(heap, *self._expand(d, p, c))))
                )  # p:dijkstra (mergeAll (h:expand d p c) g
            case None:
                return self._dijkstra(h)  # dijkstra h g
```

With a list of shortest paths, we now just need some wrapper functions to complete the implementation:

```python
class Graph(abc.ABC, typing.Generic[A, B]):
    ...

    def _spt(self, node: Node) -> "LRTree[float]":
        heap = ImmutableHeap.unit(LPath((LNode(node, 0.0),)))
        return self._dijkstra(heap)

    def sp(self, s: Node, t: Node) -> tuple[Node, ...] | None:
        return self._spt(s).get_path(t)
```

Note that there is a typo in the linked version of the paper which incorrectly defines `spt`, i.e. the shortest paths
from `t`, as

```hs
spt v = spt (unitheap [(v, 0)])
```

where it should read

```hs
spt v = dijkstra (unitheap [(v, 0)])
```

## Validation

Let’s check it works! Wikipedia has an article on Dijkstra’s algorithm where it shows a simple small graph labeled 1–6.

![An animation demonstrating Dijkstra's algorithm implemented the 'normal' way, showing an undirected, labeled graph with six nodes. Starting at the node labeled '1', the animation shows how each node is visited in turn and tagged with a value representing the shortest path to that node, until the shortest path to the destination is tagged. The final shortest path is 1, 3, 6, 5, with a total length of 20](https://upload.wikimedia.org/wikipedia/commons/5/57/Dijkstra_Animation.gif)

[_https://en.wikipedia.org/wiki/File:Dijkstra_Animation.gif_](https://en.wikipedia.org/wiki/File:Dijkstra_Animation.gif)

The shortest graph from Node 1 to Node 5 goes through 3 and 6. Given everything we’ve implemented so far, we can now
construct this graph with all the edges and test our algorithm:

```pycon
>>> graph = (
...     Context(Adj(), Node(1), 1, Adj(((7, Node(2)), (9, Node(3)), (14, Node(6)))))
...     & Context(Adj(), Node(2), 2, Adj(((10, Node(3)), (15, Node(4)))))
...     & Context(Adj(), Node(3), 3, Adj(((11, Node(4)), (2, Node(6)))))
...     & Context(Adj(), Node(4), 4, Adj(((6, Node(5)),)))
...     & Context(Adj(), Node(5), 5, Adj(((9, Node(6)),)))
...     & Context(Adj(), Node(6), 6, Adj())
...     & EmptyGraph()
... ).undir()
>>> graph.sp(Node(1), Node(5))
(1, 3, 6, 5)
```

That puts a smile on my face.

# Conclusion

We’ve seen how to implement some functional algorithms for graphs in Python, and how closely we can approach the Haskell
descriptions using Python syntax like destructuring and `match` statements. In the next and final part I’m going to give
my overall thoughts about this exercise, and draw some conclusions about functional programming in Python. See you
there!

# References

1. Erwig, Martin. “Inductive graphs and functional graph algorithms.” _Journal of Functional Programming_ 11.5 (2001):
   467–492.