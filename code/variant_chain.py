from pprint import pprint
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import agreement


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'


def iter_pairs(iterable):
	for i in range(len(iterable) - 1):
		yield iterable[i], iterable[i + 1]


class SpellingTransitions:

	def __init__(self, counts):
		self.lemmata = counts['lemma'].unique()
		self.counts = counts.groupby('lemma')
		self.seq_matcher = SequenceMatcher()
		self.transition_points = [f'{i}-{i+1}' for i in range(1, 13)]
		# self.transformations_by_point = {
		# 	f'{i}-{i+1}': defaultdict(list)
		# 	for i in range(1, 13)
		# }
		self.transformations_by_point = defaultdict(lambda: defaultdict(list))
		for lemma in self.lemmata:
			self.compute_transformations(lemma)

		
		self.uni_transformations = sorted(list(self.transformations_by_point))
		self.transition_matrix = np.zeros((len(self.uni_transformations), 12), dtype=int)
		for i, trans in enumerate(self.uni_transformations):
			for j, point in enumerate(self.transition_points):
				lemmata = self.transformations_by_point[trans][point]
				self.transition_matrix[i, j] = len(lemmata)
		for trans, row in zip(self.uni_transformations, self.transition_matrix):
			print(str(row.sum()).zfill(4), trans, row)

		
		# for transition_point, data in self.transformations_by_point.items():
		# 	sorted_transformations = sorted(list(data.keys()), key=lambda k: len(data[k]), reverse=True)
		# 	print(transition_point)
		# 	for transformation in sorted_transformations:
		# 		print(transformation, len(data[transformation]))
		# 	print()

	def make_variant_chain(self, lemma):
		counts = self.counts.get_group(lemma)
		variants = list(counts['variant'])
		variant_chain = []
		for band_i in range(1, 14):
			band_counts = counts[f'band_{band_i}'].to_numpy()
			dom_forms = agreement.determine_dominant_form(band_counts, variants)
			if dom_forms and len(dom_forms) == 1:
				dom_form = list(dom_forms)[0]
			else:
				dom_form = None
			variant_chain.append(dom_form)
		return variant_chain

	def compare(self, form1, form2):
		transformations = []
		if form1 == form2:
			return transformations
		self.seq_matcher.set_seqs(form1, form2)
		for code, f1s, f1e, f2s, f2e in self.seq_matcher.get_opcodes():
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

	def compute_transformations(self, lemma):
		variant_chain = self.make_variant_chain(lemma)
		for i, (variant1, variant2) in enumerate(iter_pairs(variant_chain), 1):
			transition_point = f'{i}-{i+1}'
			if variant1 is None or variant2 is None:
				continue
			transformations = self.compare(variant1, variant2)
			for transformation in transformations:
				self.transformations_by_point[transformation][transition_point].append(lemma)


	def plot_transformations(self, transformations):
		fig, axis = plt.subplots(1, 1, figsize=(7.48, 3))
		for transformation in transformations:
			row_i = self.uni_transformations.index(transformation)
			axis.plot(range(2, 14), self.transition_matrix[row_i], label=transformation)
		axis.set_xlabel('Time period')
		axis.set_ylabel('Number of lemmata')
		axis.set_xticks(range(2, 14))
		axis.set_xticklabels([f'Band {i}' for i in range(2, 14)])
		axis.legend()
		plt.show()



if __name__ == '__main__':

	counts_oed = pd.read_csv(DATA / 'count_oed.csv', keep_default_na=False)

	st = SpellingTransitions(counts_oed)

	# st.plot_transformations(['ie→y', 'y→ie'])
	st.plot_transformations(['f→ph', 'ph→f'])
