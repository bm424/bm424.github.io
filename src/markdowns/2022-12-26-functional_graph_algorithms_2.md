Title: Implementing Functional Graph Algorithms in Python (Part 2: Functions)
Date: 2022-12-26 00:00
---
_This article was originally published on
Medium ([link](https://medium.com/@benhmartineau/implementing-functional-graph-algorithms-in-python-part-2-functions-cf15e640c7c3))_

Hello! Welcome to the second part of this series on functional programming in Python. If you haven’t read the first part
yet, check it out [here](#2022-12-19-functional_graph_algorithms_1).

In this series, we’re implementing “inductive graphs” as described
in [this paper](https://www.cambridge.org/core/journals/journal-of-functional-programming/article/inductive-graphs-and-functional-graph-algorithms/2210F7C31A34EA4CF5008ED9E7B4EF62) (
Erwig 2001). In the first part, we
defined the basic data structures, and we’ll now move on to implementing the necessary abstract methods and some basic
algorithms. As a reminder, you can find all of the code for these articles at
the [`inductive-graph-algorithms`](https://github.com/bm424/inductive-graph-algorithms) repository
over on GitHub.

# Abstract Methods

Take a look at Table 1 in the paper. It explains that for inductive graph algorithms, we need three basic features for
the graph:

1. A test for emptiness.
2. The ability to extract an arbitrary context from the graph.
3. The ability to extract a specific context from the graph.

How we choose to implement these features is up to us. I’ve chosen to implement the test for emptiness as a property of
the graph, and the context extraction as a method `.pop(node: Optional[Node])` on the graph:

```python
class Graph(abc.ABC, typing.Generic[A, B]):
    ...

    @property
    @abc.abstractmethod
    def is_empty(self) -> bool:
        """True if the graph is empty (contains no nodes), False otherwise."""

    @abc.abstractmethod
    def pop(self, node: Node | None = None) -> tuple[Context[A, B], "Graph[A, B]"] | None:
        """Extracts a given `node` from the graph.

        Returns the node's context, and the remaining graph. If `node` is None, any
        node may be extracted. If `node` is not in the graph, returns None.
        """
```

Now let’s implement these for our subtypes! For the empty graph, it’s easy enough:

```python
class EmptyGraph(Graph[A, B]):
    ...

    @property
    def is_empty(self) -> bool:
        return True

    def pop(self, node: Node | None = None) -> tuple[Context[A, B], "Graph[A, B]"] | None:
        return None
```

The empty graph is, obviously, empty, and we can never extract any context from it.

The inductive graph implementation is more complicated:

```python
class InductiveGraph(Graph[A, B]):
    ...

    @property
    def is_empty(self) -> bool:
        return False

    def pop(self, node: Node | None = None) -> tuple[Context[A, B], "Graph[A, B]"] | None:
        if node is None or node == self.head.node:
            return self.head, self.tail
        node_context, graph_context = self.head.pop(node)
        if match := self.tail.pop(node):
            sub_node_context, subgraph = match
            return node_context | sub_node_context, graph_context & subgraph
        return None
```

Let’s dig into `pop` here.

First, if `node` is `None`, it means we can return any arbitrary context alongside the remaining graph. The way we’ve
implemented `InductiveGraph` makes this very easy — we simply return the head, which is a context, and the tail, which
by
construction never refers to any node mentioned in the head. We can do exactly the same if the specific node requested
happens to be the head node.

If neither of the two conditions above is satisfied, it’s time for some recursion! First, we take the head context and
split it into two parts. The first part contains any references to node, inverted so that `node` is the node of the
context — this is `node_context`. The second part contains any references that are not to `node`.

![An illustration of how the "head" node of a graph is decomposed into two contexts. One context, called "node_context", centres on "node", and contains only references between "node" and "head". The other context, called the "graph_context", centres on "head", and contains only any
_other_ references to "head".](graph_context_pop.png)

_Splitting the head into component parts._

Then, we try to pop `node` from `tail`, meaning that we start again with `pop`! Eventually, we must either reach `node`,
or find
that `node` is not in the graph. Either way, the recursion terminates at some point.

What happens if we reach `node`? `pop` returns a tuple of `node_context | sub_node_context`
and `graph_context & subgraph`. The
first part of this joins all of the node_contexts together into a single context - the one we want extracted! Every
reference to `node` in the graph is encapsulated in a new context with `node` at the center. The second part
re-constructs a
graph from all of the contexts which don't contain `node` - the remainder.

That's a lot of behaviour wrapped up in one little function, so let's go over it slowly once more.

1. If the head is the context of the node we need, return it and the remaining graph.
2. Otherwise, break the head into parts. One part contains any references to the node we need, the other part contains
   no references to the node we need.
3. Repeat the above process with the tail.
4. Once we have the context of the node we need, join all the contexts that do reference the node into our extracted
   context, and construct a graph from the contexts that do not reference the node.

Phew 😅 With that tricky part out the way, we can get on to some sweet implementations!

# Basic Functions

Back in Part 1, I said that we could define functions on inductive graphs analogous to `reduce` and `map` for lists.
Let's
do that now!

## `ufold()`

In the paper, `reduce` for graphs is called `ufold`. `fold` is an often-used synonym for `reduce` in functional
programming, and
`ufold` means the fold on graphs is "unordered," because the nodes are, in general, traversed in arbitrary order.

The paper describes the `ufold` function in the following way:

```hs
ufold :: (Context a b -> c -> c) -> c -> Graph a b -> c
ufold f u Empty = u
ufold f u (c & g) = f c (ufold f u g)
```

This means: take a graph, a starting value of type `c`, and a function which takes something of type `c` and a `Context`
to
produce a result `c`. `ufold` will then produce a result of type `c`. Yes, it's a higher-order function which takes
another
function as a parameter! `ufold` over an empty graph is just the starting value, but for anything else we extract an
arbitrary context, then apply the function over that context and the result of `ufold` on the remainder. More recursion!

Thankfully, this is actually pretty concise in Python:

```python
class Graph(abc.ABC, typing.Generic[A, B]):
    ...

    def ufold(self, fn: typing.Callable[[Context[A, B], C], C], u: C) -> C:
        """Un-ordered fold."""
        if self.is_empty:
            return u
        head, graph = self.pop()  # c & g
        return fn(head, graph.ufold(fn, u))  # f c (ufold f u g)
```

## `nodes()`

How do we use `.ufold()`? Well, let's say we want to get the nodes of the graph. In Haskell syntax, the function looks
like this:

```hs
nodes :: Graph a b -> [Node]
nodes = ufold (\(p, v, l, s) -> (v:)) []
```

In simple words, this says that the nodes of the graph are just appended one by one to an initially-empty list. In
Python, it looks like this:

```python
class Graph(abc.ABC, typing.Generic[A, B]):
    ...

    def nodes(self) -> tuple[Node, ...]:
        """The nodes of the graph."""
        # ufold (\(p, v, l, s) -> (v:)) []
        return self.ufold(lambda context, result: (context.node, *result), ())
```

That's pretty concise, and again it mirrors the Haskell definition pretty closely.

## `gmap()`

`gmap` is the graph's equivalent of `map` and we can use `ufold` to implement it!

```hs
gmap :: (Context a b -> Context c d) -> Graph a b -> Graph c d
gmap f = ufold (\c -> (f c &)) Empty
```

In other words, `gmap` is a function that takes a graph and a function that converts a context into another context, and
produces another graph. We can implement it by applying the function to each context, and constructing a graph from the
result. In Python:

```python
class Graph(abc.ABC, typing.Generic[A, B]):
    ...

    def gmap(
            self, fn: typing.Callable[[Context[A, B]], Context[C, D]]
    ) -> "Graph[C, D]":
        """Convert the graph into another graph via `fn` over its contexts."""
        # ufold (\c -> f c &) Empty
        return self.ufold(
            lambda context, result: fn(context) & result, EmptyGraph[C, D]()
        )
```

# Conclusion

The inductive graph definition requires just three features: a test for emptiness, the removal of an arbitrary node's
context, and the removal of a specific node's context. With those in place, we can create some very succinct functions
to form the basis of our functional graphs: `ufold`, and `gmap`.

In the next part, we'll implement some more complex algorithms including Dijkstra's algorithm and topological sorting.

# References

1. Erwig, Martin. "Inductive graphs and functional graph algorithms." _Journal of Functional Programming_ 11.5 (2001):
   467–492.