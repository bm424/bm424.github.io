Title: Build Day 2
Date: 2021-05-26 23:00
---

# print()

So, main changes today include adding support for each posts's metadata,
handling multiple posts building to the same page in the correct order,
and some small updates to improve the site's aesthetics including some
page hierarchy and correct scaling on mobile.

One of the things I find it's really important to do, particularly in personal
projects, is write a few notes to yourself to remind you simply what commands
to write to get things working again. It sounds obvious, but a lot of the actual
minutes spent on a programming project for me are spent working out the correct
order of operations.

For this project, the relevant command is a simple
```
docker-compose build && docker-compose run main
```
but in a web project with multiple moving parts these kinds of crucial lines
can be easy to forget or get lost in a maze of possible, often redundant (in
the sense of overlapping functionality) scripts. So when I write a README file,
it's as much for me as for anyone else who might pick up the project.

# .split()

One thing that came up while coding today was the issue of post permalinks.
I'm not even going to _attempt_ to go there. The quick solution I settled on
was to link to the posts using the file name. As I anticipate I'll be changing
those much less than the titles of the posts, they ought to be permanent enough,
and they map to the titles sufficiently closely to be sensible in the URL.

Come to think of it, this may be similar to what professional static site
generators do, given the mismatch between URLs and post titles that I sometimes
see.

On an unrelated note, using a NamedTuple was a good way to pass values into
the Jinja templates quickly, but it's quickly showing its limitations. I've
been using Pydantic a lot at work and I like it a lot, we'll see if I need to
get it involved here, depending on how much the complexity of the NamedTuple
structure increases.

# :focus

To wrap up, I spent a fair bit of time faffing around with the style of the
anchor links to the posts. This is actually the kind of thing I tend to find
really fun, because webpage style is one of the ways it's easy to get a little
creative in projects like this. That said, I often get carried away in style
over substance. Part of this project is to focus on getting the content out,
rather than perfecting style, so with these final changes I'm going to call
it a day and implement the GitHub pages build another time.
