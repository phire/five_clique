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

import csv
from tqdm import tqdm

# Here, now, begins the daunting task of finding five-cliques in the graph we
# prepared via 'generate_graph.py'.

print('--- loading graph ---')

# load the graph first
words = []
with open('word_graph.csv', newline='', encoding='utf-8') as f:
	reader = csv.reader(f, delimiter = '\t')
	for row in tqdm(reader):
		word = row[0]
		neighbor_string = row[1]
		neighbors = set([int(neighbor) for neighbor in neighbor_string[1:-1].split(', ')])
		words.append((row[0], neighbors))

print('--- start clique finding (THIS WILL TAKE LONG!) ---')

# start clique finding
Cliques = []
for i in tqdm(range(len(words))):
	Ni = words[i][1]
	for j in Ni:
		if j < i:
			continue
		# the remaining candidates are only the words in the intersection
		# of the neighborhood sets of i and j
		Nij = Ni & words[j][1]
		if len(Nij) < 3:
			continue
		for k in Nij:
			if k < j:
				continue
			# intersect with neighbors of k
			Nijk = Nij & words[k][1]
			if len(Nij) < 2:
				continue
			for l in Nijk:
				if l < k:
					continue
				# intersect with neighbors of l
				Nijkl = Nijk & words[l][1]
				# all remaining neighbors form a 5-clique with i, j, k, and l
				for r in Nijkl:
					if r < l:
						continue
					Cliques.append([i, j, k, l, r])

print('completed! Found %d cliques' % len(Cliques))

print('--- write to output ---')
with open('cliques.csv', 'w', newline='', encoding='utf-8') as f:
	writer = csv.writer(f, delimiter = '\t')
	for cliq in Cliques:
		# get word representation of cliques and write to output
		cliq_words = [words[i][0] for i in cliq]
		writer.writerow(cliq_words)
