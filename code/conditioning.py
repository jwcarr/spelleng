from collections import defaultdict
from pathlib import Path
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt

plt.rcParams.update({'font.sans-serif': 'Helvetica Neue', 'font.size': 7})


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'


band_headers = [f'band_{i}' for i in range(1, 14)]


colors = ['cadetblue', 'crimson', 'DarkOrange', 'green', 'purple', 'black', 'gray', 'brown']


class VarCounter:

	def __init__(self, counts, grapheme_variants, position):
		self.grapheme_variants = grapheme_variants
		if position == 'initial':
			self.grapheme_variants_re = re.compile(r'^(?P<var>' + '|'.join(grapheme_variants) + r')\w+')
		elif position == 'medial':
			self.grapheme_variants_re = re.compile(r'\w+?(?P<var>' + '|'.join(grapheme_variants) + r')\w+')
		elif position == 'final':
			self.grapheme_variants_re = re.compile(r'\w+?(?P<var>' + '|'.join(grapheme_variants) + r')$')
		else:
			raise ValueError('Invalid position argument')
		self.counts_grouped = counts.groupby('lemma')
		self.variant_counts = np.zeros((len(grapheme_variants), 13), dtype=int)

	def count_lemma(self, lemma):
		lemma_counts = self.counts_grouped.get_group(lemma)
		variant_spellings = list(lemma_counts['variant'])
		for variant in variant_spellings:
			if var_match := self.grapheme_variants_re.match(variant):
				grapheme = var_match['var']
				grapheme_index = self.grapheme_variants.index(grapheme)
				self.variant_counts[grapheme_index] += lemma_counts[ lemma_counts['variant'] == variant ][band_headers].values.flatten()

	def count_all_matching_lemmata(self, target_pos=None):
		for lemma in self.counts_grouped.groups.keys():
			wordform, pos = lemma.split('_')
			if target_pos is None or target_pos == pos:
				if var_match := self.grapheme_variants_re.match(wordform):
					self.count_lemma(lemma)
	
	def get_variant_proportions(self):
		proportions = np.zeros(self.variant_counts.shape, dtype=float)
		for i in range(13):
			if total := self.variant_counts[:, i].sum():
				proportions[:, i] = self.variant_counts[:, i] / total
		return proportions


def plot_variants_over_time(axis, var_counter, linestyle):
	proportions = var_counter.get_variant_proportions()
	# proportions = var_counter.variant_counts
	for i, grapheme_var in enumerate(var_counter.grapheme_variants):
		axis.plot(range(1, 14), proportions[i], label=grapheme_var, linestyle=linestyle, color=colors[i])
	axis.set_ylim(-0.05, 1.05)
	axis.set_xlim(0.5, 13.5)
	axis.set_xticks(range(1, 14))
	axis.set_xticklabels(range(1, 14))
	axis.set_ylabel('Usage proportion')
	axis.set_xlabel('Historical band')


def plot_specialization(axis, var_counter1, var_counter2):
	proportions1 = var_counter1.get_variant_proportions()
	proportions2 = var_counter2.get_variant_proportions()
	specialization = proportions1 - proportions2
	for i, grapheme_var in enumerate(var_counter1.grapheme_variants):
		axis.plot(range(1, 14), specialization[i], label=grapheme_var, color=colors[i])
	axis.set_ylim(-0.55, 0.55)
	axis.set_xlim(0.5, 13.5)
	axis.set_xticks(range(1, 14))
	axis.set_xticklabels(range(1, 14))
	axis.set_ylabel('Specialization quotient')
	axis.set_xlabel('Historical band')


def make_plot():
	pass



if __name__ == '__main__':

	count_quot = pd.read_csv(DATA / 'count_text.csv')

	fig, axes = plt.subplots(1, 2, figsize=(7.48, 2))


	interesting_variants = {
		'k_initial': {
			# 'grapheme_variants': ['cque', 'que', 'che', 'cke', 'ck', 'ke', 'k', 'c'],
			'grapheme_variants': ['ch', 'c', 'k', 'q'],
			'position': 'initial',
		},
		'k_final': {
			# 'grapheme_variants': ['cque', 'que', 'che', 'cke', 'ck', 'ke', 'k', 'c'],
			'grapheme_variants': ['cke', 'ck', 'ke', 'k', 'c'],
			'position': 'final',
		},
		'f_initial': {
			'grapheme_variants': ['ph', 'f'],
			'position': 'initial',
		},
		'f_final': {
			'grapheme_variants': ['ph', 'ff', 'gh', 'f'],
			'position': 'final',
		},
		's_final': {
			'grapheme_variants': ['ss', 'ce', 'se', 's', 'c'],
			'position': 'final',
		},
	}

	# make_plot(interesting_variants['k_final'])

	var_counter_noun = VarCounter(count_quot, **interesting_variants['k_initial'])
	var_counter_noun.count_all_matching_lemmata(target_pos='n')
	plot_variants_over_time(axes[0], var_counter_noun, linestyle='-')
	axes[0].legend(frameon=False)

	var_counter_verb = VarCounter(count_quot, **interesting_variants['k_initial'])
	var_counter_verb.count_all_matching_lemmata(target_pos='v')
	plot_variants_over_time(axes[0], var_counter_verb, linestyle='--')

	plot_specialization(axes[1], var_counter_noun, var_counter_verb)

	fig.tight_layout(pad=0.5, h_pad=1.0, w_pad=2.0)

	fig.savefig(ROOT / 'manuscript' / 'figs' / 'specialization_k_initial.pdf')


