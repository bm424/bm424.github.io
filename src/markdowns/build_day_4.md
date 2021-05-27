Title: Build Day 4
Date: 2021-05-27 22:00
---

# commit

Today we publish. The plan is to use GitHub pages, which at first glance seemed
pretty simple but none of the documentation immediately points to hwo to run
the repo through a build process before publication. So finding that out is
the immediate priority.

---

Half an hour in and this is not nearly as easy as I expected. It seems these
custom builds just aren't really a part of the GitHub ecosystem and... I get
that... but I really think it ought to be achievable with GitHub actions.

# tag

And another half an hour later and we're live at https://bm424.github.io/ !
Turned out to be not that difficult, just a heavy reliance on existing published
actions, which isn't something I'm very used to.

I'm going to write down what happened for my own future reference.

## Self-Tutorial

There are three basic steps needed:

1. Checkout your own repository. This is accomplished using the public
   "checkout" action, visitable (here)[https://github.com/actions/checkout].
   This is surprising to me, as I'd have assumed this was more or less an
   automatic part of the process, but I suppose explicitly doing this is better
   than implicitly assuming it.
2. Create a version of your _own_ build action. This was actually pretty
   simple, you can directly reference your own Docker image and the entire
   source repo is mounted in, so as long as you're using relative file names
   (normally a sad accident, but here a happy one) it pretty much successfully
   built first time, although I was a little confused about where the action
   was supposed to live (turns out top-level in the repo is fine).
3. Use yet another public image, this one sourced from a nice little tutorial
   (here)[https://www.pluralsight.com/guides/how-to-host-your-static-webpages-on-github-pages],
   to push the site to your branch. A quick skim through the source code
   suggests this does much of the same manual stuff one might have implemented
   (git push to branch etc) but packaged up nice.

Moving forward, I'm hoping I'll remember to refer to this repo as a canonical
example for myself.
