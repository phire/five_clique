# Five Clique

Copyright (C) 2022 - Benjamin Paassen, Scott Mansell

A solution to the problem of finding five English words with 25 distinct characters, using graph theory.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

## Description

This is a fork of Benjamin's solution to Matt Parker's "five five-letter words with twenty-five unique letters" problem. 

Benjamin's solution can be found here: https://gitlab.com/bpaassen/five_clique

After viewing [Matt's youtube video](https://www.youtube.com/watch?v=_-AfhLQfb6w&t=1s) which covers
the problem, Matt's solution to the problem and then Benjamin's solution, I was inspired (nerd-sniped)
into trying to optimize it further.

I was originally planning to do a sneaky conversion into c or c++, and claim the free performance gains
that such ports usually get.
But it's always a good idea to make sure the original algorithm is somewhat optimal before porting
to another language, you don't want to be doing two things at once.

And despite Benjamin's mocking readme description (which I've preserved below), and experience writing
computer-science research papers, they left a lot of low-hanging fruit just sitting there for someone
like me (who can't even be bothered finishing their computer science degree) to improve on. 

But Benjamin gave it a go. And that's something.

*Benjamin dissed Matt, it's only fair I pass on the diss :)*

### Improvements

 * Anagrams are filtered out before building the graph. 
   The filtering cuts the number of nodes by about 40%, and removes a lot of duplicate paths. The size
   of the serialized graph drops from 87MB to just 36MB; Execution time drops from 19.5min to 5.5min on
   my machine, a 3-4x performance gain. 
   This was in Matt Parker's original solution. 
 * Character sets were replaced with a bitset, that represents words with one bit per letter of the
   alphabet. We can get away with this, since there are no duplicate letters allowed. 
 * Pruning was added to the main search. 
   We keep track of branches that have been proven to not contain results, and avoid re-calculating
   them. This provides a 6-7x speedup. 
 * The two steps were merged, which eliminated the time needed to serialize and deserialize the graph.
   With the other optimizations, this was now a major bottleneck
 * (Contributed by @dougallj, twitter) Move the one-way relationship test from the O(n^5) search loop,
   to the the O(n^2) neighborhood building loop. This reduces significant strain on more expensive loop
   and results in a 2-3x speedup
 * (Contributed by Dinoguy1000, gitlab) Fix typo that checked len(Nij) instead of len(Nijk)
   It's about a 5% speedup
 * Various small optimizations to the O(n^5) loop. It's really sensitive, especially in cpython

With these improvement, execution time on my machine with regular python improves from 19.5min to just
14.5 seconds. Replacing cpython with pypy improves things further to about 5 seconds. 

### Failed optimization ideas

You might notice that I kept Benjamin's core algorithm, with it's O(n^5) worst case. 

I did spend a bit of time trying to work out alternative solutions, with much better computational 
complexity. But my tests always ended up slower than the raw O(n^5) loop (and this was before I
even implemented pruning)

Part of the problem is that the average case is nowhere near the worst case. The other part is related
to memory bandwidth and caches; Modern CPUs do not match the theoretical model used by computational 
complexity and ny experiments tended to massively increase memory bandwidth. 

Once I added the pruning, nothing else could come close. Sometimes the real-world is weird like that. 

*If you can work out a better algorithm, you are required to diss me in your readme, like I dissed
Benjamin before me, and Benjamin dissed Matt before him*

## Quickstart guide

To reproduce my calculation, please execute the following steps:

1. Download the `words_alpha.txt` file from https://github.com/dwyl/english-words (this is the same file that Parker used).
2. Run the `five_cliques.py` file. (should take at most a few min)

All five-word groups with distinct letters should then be in the file `cliques.csv`.


## Benjamin's original Description

This solution is inspired by the wonderful [A problem squared podcast](https://aproblemsquared.libsyn.com/) by Hill and Parker. In episode 38, Hill and Parker are searching for five English words with distinct letters. Parker's proposed solution builds pairs of distinct words and then tries to merge these pairs to groups of five (henceforth named 'The Parker algorithm'). According to Parker, executing Parker's algorithm on a laptop took about a month. This appeared to the author as optimizable.

The solution proposed here represents the problem as a graph. In particular, we consider all 5-letter words (without repeated letters) of the English language as nodes in a graph, and we say that two words are neighbors if they share no letters. Finding 5 words with distinct letters now is equivalent to finding a [5-clique](https://en.wikipedia.org/wiki/Clique_(graph_theory)) in this graph, meaning a cluster of 5 words where each word is neighbor to each other word in the cluster.

How do we find a 5-clique, then? We start at some word i and build a clique from there. First, we consider all neighbors j. The third word k in the clique now needs to be neighbor to both i and j. Therefore, we consider only words k in the intersection of the neighbor sets of i and j. Next, we consider words l in the intersection of the neighbor sets of i, j, and k. Finally, any words r in the intersection of the neighbor sets of i, j, k, and l form a 5-clique {i, j, k, l, r}. To avoid repitions, we only consider solutions where i < j < k < l < r.

In the worst case, this scheme has a complexity of O(n^5), where n is the number of 5-letter words in the English language. This may seem infeasible. However, the size of the intersection rapidly declines the deeper we go into the clique. Therefore, we are finished in 21 minutes and 46 seconds, rather than a month, as in the Parker algorithm.

But Parker gave it a go. And that's something.