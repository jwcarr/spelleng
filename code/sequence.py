from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'


def iter_pairs(iterable):
	for i in range(len(iterable) - 1):
		yield iterable[i], iterable[i + 1]


class SpellingTransitions:

	def __init__(self, counts):
		self.counts = counts.groupby('lemma')
		self.sequence_matcher = SequenceMatcher()
		self.transition_points = [f'{i}-{i+1}' for i in range(1, 13)]
		self.transformations_by_transition_point = {
			transition_point: defaultdict(list)
			for transition_point in self.transition_points
		}

	def _compare_strings(self, form1, form2):
		transformations = []
		if form1 == form2:
			return transformations
		self.sequence_matcher.set_seqs(form1, form2)
		for code, f1s, f1e, f2s, f2e in self.sequence_matcher.get_opcodes():
			if code == 'replace':
				part1 = form1[f1s:f1e]
				part2 = form2[f2s:f2e]
				transformations.append(f'{part1}→{part2}')
			elif code == 'delete':
				deletion = form1[f1s:f1e]
				transformations.append(f'-{deletion}')
			elif code == 'insert':
				insertion = form2[f2s:f2e]
				transformations.append(f'+{insertion}')
		return transformations

	def compute_transformations(self, lemma, band1, band2):
		lemma_counts = self.counts.get_group(lemma)

		lemma_counts_band1 = lemma_counts[ (lemma_counts[band1] > 0) ]
		variants1 = list(lemma_counts_band1['variant'])
		counts1 = list(lemma_counts_band1[band1])

		lemma_counts_band2 = lemma_counts[ (lemma_counts[band2] > 0) ]
		variants2 = list(lemma_counts_band2['variant'])
		counts2 = list(lemma_counts_band2[band2])

		print(variants1, counts1)
		print(variants2, counts2)
		quit()
		for i, (variant1, variant2) in enumerate(iter_pairs(variant_chain), 1):
			transition_point = f'{i}-{i+1}'
			if variant1 is None or variant2 is None:
				continue
			transformations = self._compare_strings(variant1, variant2)
			for transformation in transformations:
				self.transformations_by_point[transformation][transition_point].append(lemma)


if __name__ == '__main__':

	counts_oed = pd.read_csv(DATA / 'count_oed.csv', keep_default_na=False)

	st = SpellingTransitions(counts_oed)

	st.compute_transformations('king_n', 'band_1', 'band_2')

	# 	for lemma in self.lemmata:
	# 	self.compute_transformations(lemma)
	# self.uni_transformations = sorted(list(self.transformations_by_point))
	# self.transition_matrix = np.zeros((len(self.uni_transformations), 12), dtype=int)
	# for i, trans in enumerate(self.uni_transformations):
	# 	for j, point in enumerate(self.transition_points):
	# 		lemmata = self.transformations_by_point[trans][point]
	# 		self.transition_matrix[i, j] = len(lemmata)
	# for trans, row in zip(self.uni_transformations, self.transition_matrix):
	# 	print(str(row.sum()).zfill(4), trans, row)
