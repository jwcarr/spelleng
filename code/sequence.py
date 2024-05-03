from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'


class SpellingTransitions:

	def __init__(self, n_bands=13):
		self.n_bands = n_bands
		self.sequence_matcher = SequenceMatcher()
		self.transition_points = [(i, i + 1) for i in range(1, n_bands)]
		self.transformations_by_transition_point = {
			transition_point: defaultdict(list)
			for transition_point in self.transition_points
		}
		self.transformation_counts = {}

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

	def _process_transition(self, variants, transition_point, band_a_counts, band_b_counts, pos):
		if band_a_counts.sum() > 0:
			band_a_probs = band_a_counts / band_a_counts.sum()
		else:
			band_a_probs = np.zeros(len(variants))
		if band_b_counts.sum() > 0:
			band_b_probs = band_b_counts / band_b_counts.sum()
		else:
			band_b_probs = np.zeros(len(variants))
		transition_probs = np.outer(band_a_probs, band_b_probs)
		for a, variant_a in enumerate(variants):
			for b, variant_b in enumerate(variants):
				if transition_probs[a, b] == 0:
					continue
				transformations = self._compare_strings(variant_a, variant_b)
				for transformation in transformations:
					self.transformations_by_transition_point[transition_point][f'{pos}:{transformation}'].append(
						transition_probs[a, b]
					)

	def _process_lemma(self, lemma_counts, pos):
		variants = list(lemma_counts['variant'])
		variants = [re.sub('e$', 'ë', variant) for variant in variants]
		for band_a in range(1, self.n_bands):
			band_b = band_a + 1
			transition_point = (band_a, band_b)
			band_a_counts = lemma_counts[f'band_{band_a}'].to_numpy()
			band_b_counts = lemma_counts[f'band_{band_b}'].to_numpy()
			self._process_transition(variants, transition_point, band_a_counts, band_b_counts, pos)

	def create_transformation_counts(self):
		transformation_counts = defaultdict(int)
		for transition_point in self.transition_points:
			for transformation, probs in self.transformations_by_transition_point[transition_point].items():
				transformation_counts[transformation] += len(probs)
		self.transformation_counts = {
			k: transformation_counts[k]
			for k in sorted(transformation_counts, key=lambda k: transformation_counts[k], reverse=True)
		}

	def compute(self, counts):
		counts_by_lemma = counts.groupby('lemma')
		lemmata = counts['lemma'].unique()
		for i, lemma in enumerate(lemmata):
			if i % 1000 == 0:
				print(i, lemma)
			# if i == 1000:
			# 	break
			pos = lemma[-1]
			self._process_lemma( counts_by_lemma.get_group(lemma), pos )
		self.create_transformation_counts()

	def get_transformation_timecourse(self, transformation, pos):
		timecourse = []
		for transition_point in self.transition_points:
			transformations = self.transformations_by_transition_point[transition_point]
			transformation_probs = transformations[f'{pos}:{transformation}']
			if transformation_probs:
				timecourse.append(sum(transformation_probs) / len(transformation_probs))
			else:
				timecourse.append(0)
		return np.array(timecourse)


def plot_timecourse(st, transformation1, transformation2):
	transformation = f'{transformation1}→{transformation2}'
	transformation_inv = f'{transformation2}→{transformation1}'

	linestyles = {'n': '-', 'j': '--', 'v': ':'}
	colors = {'n': 'cadetblue', 'j': 'DarkOrange', 'v': 'crimson'}
	labels = {'n': 'Noun', 'j': 'Adjective', 'v': 'Verb'}

	fig, axis = plt.subplots(1, 1, figsize=(6, 3))
	# for color, transformation in zip(['cadetblue', 'crimson'], transformations):

	axis.axhline(0, color='black', linewidth=1)

	axis.text(5.5, 0.5, transformation, fontsize=60, verticalalignment='center', horizontalalignment='center', color='black', zorder=0, alpha=0.1)
	axis.text(5.5, -0.5, transformation_inv, fontsize=60, verticalalignment='center', horizontalalignment='center', color='black', zorder=0, alpha=0.1)

	for pos in ['n', 'v', 'j']:
		timecourse = st.get_transformation_timecourse(transformation, pos)
		timecourse_inv = st.get_transformation_timecourse(transformation_inv, pos)
		timecourse = timecourse - timecourse_inv
		# axis.plot(timecourse, label=pos, color='black', linestyle=linestyles[pos])
		axis.plot(timecourse, label=labels[pos], color=colors[pos], linewidth=5, alpha=0.7)
	axis.set_xticks(range(len(st.transition_points)))
	# axis.set_xticklabels([f'{band_a} → {band_b}' for band_a, band_b in st.transition_points])
	axis.set_xticklabels([f'{band_b}' for band_a, band_b in st.transition_points])
	axis.set_ylim(-1, 1)
	axis.legend()
	fig.savefig(f'/Users/jon/Desktop/transformations/{transformation}.pdf')


if __name__ == '__main__':

	counts_oed = pd.read_csv(DATA / 'count_oed.csv', keep_default_na=False)

	st = SpellingTransitions()
	st.compute(counts_oed)

	# for transition in st.transformations_by_transition_point:
	# 	print(transition)
	# 	for tfmtn, probs in st.transformations_by_transition_point[transition].items():
	# 		print('  ', tfmtn, sum(probs))
	print(st.transformation_counts)

	plot_timecourse(st, 'i', 'y')
	plot_timecourse(st, 'que', 'ck')
	plot_timecourse(st, 's', 'z')
	plot_timecourse(st, 'ȝ', 'gh')
	plot_timecourse(st, 'oo', 'u')
	plot_timecourse(st, 'ië', 'y')
	plot_timecourse(st, 'u', 'v')
	plot_timecourse(st, 's', 'c')
	plot_timecourse(st, 'c', 'k')
	plot_timecourse(st, 'þ', 'th')
	plot_timecourse(st, 'i', 'j')
	plot_timecourse(st, 'cy', 'ti')
	plot_timecourse(st, 'f', 'ph')
	
	


	
