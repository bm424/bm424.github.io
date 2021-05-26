Title: Build Day 1
Date: 2021-05-23
---
# import

A couple of hours later and we have a working static site builder running
locally using Docker, Python, Jinja2, markdown, and not much else. On the
whole I'm pretty happy with the timing, particularly considering a fairly
significant chunk of that was actually writing the build day 0 content.

I initially thought I'd be needing a running server to see changes live, but
quickly realised that was going to be unnecessary - the Docker rebuild was
more than quick enough to get a fast feedback loop going, and the most
fiddly bit, the CSS, I could actually just do in the build styles, refreshing
the page in the meantime, then copy back into the source when done.

# next()

Simple enough so far. However, having now added this next file, I need to make
a couple of changes to ensure one can navigate to past entries, and then it
should be a simple case of deploying to GitHub pages.

I say that. I've done it before, but quite a long time ago (my company uses
GitLab, so I'm a little out of practice)... so see you in the next entry.

# wraps()

I've slightly backdated this post because these reflections were based on the
hour or two of work I did after writing the first day's post a couple of days
ago, and I want to spend a bit of time after today (2021-05-26) reflecting
on today's work instead. Just for transparency's sake...
