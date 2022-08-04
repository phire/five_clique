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
	for char in word:
		alphaIndex = (ord(char) | 0x20) - ord('a')
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
		graph[char_set]	= set()

print('--- building neighborhoods ---')

# compute the 'neighbors' for each word, i.e. other words which have entirely
# distinct letters
words = sorted(list(anagrams.keys()))
for char_set in tqdm(words, total=len(words)):
	neighbors = graph[char_set]
	for i, other_set in enumerate(words):
		if char_set & other_set == 0:
			neighbors.add(i)

print('--- start clique finding (THIS WILL TAKE LONG!) ---')

# start clique finding
graphs = [graph[i] for i in words]
Cliques = []
for i in tqdm(range(len(words))):
	Ni = graphs[i]
	for j in Ni:
		if j < i:
			continue
		# the remaining candidates are only the words in the intersection
		# of the neighborhood sets of i and j
		Nij = Ni & graphs[j]
		if len(Nij) < 3:
			continue
		for k in Nij:
			if k < j:
				continue
			# intersect with neighbors of k
			Nijk = Nij & graphs[k]
			if len(Nij) < 2:
				continue
			for l in Nijk:
				if l < k:
					continue
				# intersect with neighbors of l
				Nijkl = Nijk & graphs[l]
				# all remaining neighbors form a 5-clique with i, j, k, and l
				for r in Nijkl:
					if r < l:
						continue
					Cliques.append([i, j, k, l, r])

print('completed! Found %d cliques' % len(Cliques))

def RecursiveExpand(lst):
	head, *tail = lst
	if not tail:
		return [[w] for w in anagrams[words[head]]]
	tail = RecursiveExpand(tail)

	return [[w, *t] for w in anagrams[words[head]] for t in tail]

ExpandedCliques = []
for cliq in Cliques:
	ExpandedCliques += [sorted(c) for c in RecursiveExpand(cliq)]

print(f'expanded to {len(ExpandedCliques)} cliques: %d with anagrams')

print('--- write to output ---')
with open('cliques.csv', 'w', newline='', encoding='utf-8') as f:
	writer = csv.writer(f, delimiter = '\t')

	for cliq_words in sorted(ExpandedCliques):
		writer.writerow(cliq_words)
