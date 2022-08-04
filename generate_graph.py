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


print('--- write to output ---')
with open('word_graph.csv', 'w', newline='', encoding='utf-8') as f:
	writer = csv.writer(f, delimiter = '\t')
	for i, char_set in tqdm(enumerate(words)):
		writer.writerow([anagrams[char_set][0], str(list(sorted(graph[char_set])))])

with open('anagrams.csv', 'w', newline='', encoding='utf-8') as f:
	writer = csv.writer(f, delimiter = '\t')
	for key in anagrams:
		writer.writerow([key, *anagrams[key]])
