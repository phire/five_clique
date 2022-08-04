"""
# Copyright (C) 2022 - Benjamin Paassen

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from tqdm import tqdm
import csv

# prepare a data structure for all five-letter words in string and set representation
anagrams = {}
graph = {}

# This is a compact representation of a "char set" that fits in just 26 bits
# each bit represents a letter in the alphabet
# we can quickly check for an intersection between two words with the bitwise AND operator
# or union them with bitwise OR
def alphaBit(word):
	ret = 0
	for char in word.lower():
		alphaIndex = ord(char) - ord('a')
		ret |= 1 << alphaIndex
	return ret

def bitCount(num):
	#return num.bit_count() # faster, but requires python 3.10+
	count = 0
	while num:
		num &= num - 1
		count += 1
	return count

print('--- reading words file ---')

# words_alpha.txt from https://github.com/dwyl/english-words
with open('words_alpha.txt') as f:
	for word in tqdm(f):
		word = word[:-1]
		if len(word) != 5:
			continue
		# compute set representation of the word
		char_set = alphaBit(word)
		if bitCount(char_set) != 5:
			continue

		if char_set in anagrams:
			anagrams[char_set].append(word)
			continue

		anagrams[char_set] = [word]

print('--- building neighborhoods ---')

# compute the 'neighbors' for each word, i.e. other words which have entirely
# distinct letters
for char_set in tqdm(sorted(anagrams.keys())):
	for other_set, neighbours in graph.items():
		if not other_set & char_set:
			neighbours.add(char_set)
	graph[char_set] = set()

print('--- finding cliques ---')

# We maintain a set of tree branches that we have already visited and know
# don't contain any clique subsets
#
# For performance reasons, it's only worth pruning layers 2 and 3
# layer 1 is already cached with the neighbor calculation above, and if you
# get to layer 4, it's quicker to just complete the search
prune = set()

# start clique finding
Cliques = []
for i, Ni in tqdm(graph.items()):
	for j in Ni:
		ij = i | j
		if ij in prune:
			continue
		# the remaining candidates are only the words in the intersection
		# of the neighborhood sets of i and j
		Nij = Ni & graph[j]
		if len(Nij) < 3:
			prune.add(ij)
			continue

		have_ij = False
		for k in Nij:
			ijk = ij | k
			if ijk in prune:
				continue
			# intersect with neighbors of k
			Nijk = Nij & graph[k]
			if len(Nij) < 2:
				prune.add(ijk)
				continue

			have_ijk = False
			for l in Nijk:
				# intersect with neighbors of l
				Nijkl = Nijk & graph[l]
				# all remaining neighbors form a 5-clique with i, j, k, and l
				for r in Nijkl:
					Cliques.append([i, j, k, l, r])
					have_ij = True
					have_ijk = True

			if not have_ijk:
				# we didn't find anything on this branch, prune it
				prune.add(ijk)
		if not have_ij:
			# we didn't find anything on this branch, prune it
			prune.add(ij)

print('completed! Found %d cliques' % len(Cliques))
print(f'{len(prune)} branches of the tree were pruned')

def RecursiveExpand(lst):
	head, *tail = lst
	if not tail:
		return [[w] for w in anagrams[head]]
	tail = RecursiveExpand(tail)

	return [[w, *t] for w in anagrams[head] for t in tail]

ExpandedCliques = []
for cliq in Cliques:
	ExpandedCliques += [sorted(c) for c in RecursiveExpand(cliq)]

print(f'expanded to {len(ExpandedCliques)} cliques: %d with anagrams')

print('--- write to output ---')
with open('cliques.csv', 'w', newline='', encoding='utf-8') as f:
	writer = csv.writer(f, delimiter = '\t')

	for cliq_words in sorted(ExpandedCliques):
		writer.writerow(cliq_words)
