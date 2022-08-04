# Five Clique

Copyright (C) 2022 - Benjamin Paassen  

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

This solution is inspired by the wonderful [A problem squared podcast](https://aproblemsquared.libsyn.com/) by Hill and Parker. In episode 38, Hill and Parker are searching for five English words with distinct letters. Parker's proposed solution builds pairs of distinct words and then tries to merge these pairs to groups of five (henceforth named 'The Parker algorithm'). According to Parker, executing Parker's algorithm on a laptop took about a month. This appeared to the author as optimizable.

The solution proposed here represents the problem as a graph. In particular, we consider all 5-letter words (without repeated letters) of the English language as nodes in a graph, and we say that two words are neighbors if they share no letters. Finding 5 words with distinct letters now is equivalent to finding a [5-clique](https://en.wikipedia.org/wiki/Clique_(graph_theory)) in this graph, meaning a cluster of 5 words where each word is neighbor to each other word in the cluster.

How do we find a 5-clique, then? We start at some word i and build a clique from there. First, we consider all neighbors j. The third word k in the clique now needs to be neighbor to both i and j. Therefore, we consider only words k in the intersection of the neighbor sets of i and j. Next, we consider words l in the intersection of the neighbor sets of i, j, and k. Finally, any words r in the intersection of the neighbor sets of i, j, k, and l form a 5-clique {i, j, k, l, r}. To avoid repitions, we only consider solutions where i < j < k < l < r.

In the worst case, this scheme has a complexity of O(n^5), where n is the number of 5-letter words in the English language. This may seem infeasible. However, the size of the intersection rapidly declines the deeper we go into the clique. Therefore, we are finished in 21 minutes and 46 seconds, rather than a month, as in the Parker algorithm.

But Parker gave it a go. And that's something.

## Quickstart guide

To reproduce my calculation, please execute the following steps:

1. Download the `words_alpha.txt` file from https://github.com/dwyl/english-words (this is the same file that Parker used).
2. Run the `five_cliques.py` file. (should take at most a few min)

All five-word groups with distinct letters should then be in the file `cliques.csv`.
