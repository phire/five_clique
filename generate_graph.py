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
words = []
anagrams = {}

print('--- reading words file ---')

# words_alpha.txt from https://github.com/dwyl/english-words
with open('words_alpha.txt') as f:
	for word in tqdm(f):
		word = word[:-1]
		if len(word) != 5:
			continue
		# compute set representation of the word
		char_set = set(word)
		if len(char_set) != 5:
			continue

		sorted_chars = ''.join(sorted(char_set))

		if sorted_chars in anagrams:
			anagrams[sorted_chars].append(word)
			continue

		anagrams[sorted_chars] = [word]

		# append the word, the set of characters in the word, and an empty set
		# for all the 'neighbors' of the word, which we will compute later
		words.append((word, char_set, set()))

print('--- building neighborhoods ---')

# compute the 'neighbors' for each word, i.e. other words which have entirely
# distinct letters
for i in tqdm(range(len(words))):
	char_set  = words[i][1]
	neighbors = words[i][2]
	for j in range(len(words)):
		if len(char_set & words[j][1]) == 0:
			neighbors.add(j)

print('--- write to output ---')
with open('word_graph.csv', 'w', newline='', encoding='utf-8') as f:
	writer = csv.writer(f, delimiter = '\t')
	for i in tqdm(range(len(words))):
		writer.writerow([words[i][0], str(list(sorted(words[i][2])))])

with open('anagrams.csv', 'w', newline='', encoding='utf-8') as f:
	writer = csv.writer(f, delimiter = '\t')
	for key in anagrams:
		writer.writerow([key, *anagrams[key]])
