Title: Build Day 4
Date: 2021-07-08 22:30
---
So; a couple of months later, a glass of wine in hand, with football apparently coming home, I'd like to reflect a little on why there has been such a long break between Build Days 3 and 4, and think a little bit more critically about some of the projects that I'd like to tackle going forward.

I'd started right away on the next project.
The plan was (seemed) quite simple.
I wanted a webapp - something to flex the old TypeScript muscles - which would be a searchable, interactive view of the whole Dinosaur family tree, starting with the earliest proto-dinosaurs and running through to the last species left alive when the meteorite hit.
I've always had an interest in dinosaurs (especially when younger - my mum once sent me in on a dress-up day as a paleontologist) and it seemed like a fun way to revisit some of that while having a go at a new build that I don't think has been attempted before.
How naïve I was.

Let me break down a couple of the challenges I faced.

# 1. The Challenge of Trees

I love me a tree structure.
I guess you could call me a linear algebraist by training (my PhD focused on things like [NMF](https://en.wikipedia.org/wiki/Non-negative_matrix_factorization) and data clustering) so graphs, nodes, and trees are something of a new language to me, but I've been using heirarchical structures for some frontend stuff at work and thinking about tree types in TypeScript got me really interested.
Feeling complacent (a family tree is just a tree, right?) I immediately charged down the route of encoding all the different taxonomic ranks (Genus, Class, Phylum and so on) as nodes in my future tree structure.

That idea fell apart pretty quickly, because as soon as I started looking at how to structure the actual _cladograms_ (new bit of vocab for me there), I realised that many, if not most nodes didn't actually have a taxonomic rank ascribed to them.
Thinking back, that makes total sense.
The classification of a species clearly doesn't depend strictly on its actual evolution.
If that were true, then any given dinosaur species would simply have fewer entries in its classification tree than a modern animal.
The classification is actually _closer_ to the vector/cluster description of a species than its family tree description.

Instead of simply grouping by phylum/class/order/family/genus/species, I'd have to take a much more sophisticated approach to encoding the family tree of each dinosaur.
No problem; more work, no doubt, and a less nicely-structured output (lots of nesting necessary) but doable.


I quickly ran into challenge 2.

# 2. The Challenge of Actual Science™

Although I'd anticipated challenges like the one above (it's a technical problem, after all, and creating good data structures is part of all coding) this next problem was not only the one that's slightly scuppered the project, but one I totally failed to see coming.

It turns out that - shockedpikachu.jpg - science isn't done.
In other words, there is _ongoing research_ into the family trees of dinosaurs.
I know!

I'd decided to start small, work on the Lambeosauridae family first to nail down the interface and the data structures before working in the rest of the group.
It was going well - I'd marshalled a small set of species, arranged a tree for them, and was about ready to start coding up the frontend when I realised there was going to be a real logical problem.

What happens when scientists disagree about the tree?

Naively I thought I might be able to present a menu of options to the end user.
"Would you like Prieto-Marquez 2013 or 2015 \[citation\]?"
That by itself would be fine apart from the problem of tree-hopping species.
Depending on who you talk to, for instance, [Arenysaurus](https://en.wikipedia.org/wiki/Arenysaurus) is either _deep_ into the Lambeosaurini tribe _or_ totally outside it!
Crazy!

Nightmare!

From a coding perspective this does actually pose some serious logical problems.
Let's say I've picked (higher up the tree) some cladogram proposed which shuffles around the Lambeosaurini tribe.
We then have no way of knowing which of the two proposed cladograms for Arenysaurus is compatible.
It's simply not possible to reconcile the trees.

# What's to be done?

Now if I were going to be _really_ sophisticated, I could take some of the algorithms that are used to _generate_ the cladograms and expose _those_ to the end-user.
That way, they could rearrange the whole tree at will in a nice interactive manner, and moreover perhaps explore some of the interesting differences between them.

That, however, is a much bigger project than I can take on (though the prospect of a second PhD _is_ tempting).
For now, I'm going to have to let sleeping dinosaurs lie, and instead have a crack at something more manageable.

Until the next one, whenever that is.
