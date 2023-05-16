from collections import defaultdict
from pathlib import Path
from utils import json_read, json_write
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).parent.parent.resolve()


BANDS = ['Old English', 'Middle English', 'Early Modern English']
lemma_map = json_read(ROOT / 'data' / 'lemma_map.json')


def plot_meaning(meaning):
	attested_forms_by_band = lemma_map[meaning]
	print(attested_forms_by_band)
	all_attested_forms = []
	for band, forms in attested_forms_by_band.items():
		all_attested_forms.extend(forms)
	all_attested_forms = list(set(all_attested_forms))
	all_attested_forms.sort()
	print(all_attested_forms)
	proportions = []
	for band, form_count in attested_forms_by_band.items():
		counts = []
		for form in all_attested_forms:
			n = form_count.get(form, 0)
			counts.append(n)
		counts = np.array(counts)
		proportions.append( counts / counts.sum() )
	proportions = np.array(proportions)
	print(proportions)

	stack = []
	for i in range(proportions.shape[1]):
		d = proportions[:, i]
		if stack:
			stack.append(d + stack[-1])
		else:
			stack.append(d)
	stack = np.array(stack)

	fig, axis = plt.subplots(1, 1)

	axis.stackplot([0, 1, 2], stack)
	plt.show()
	quit()

	for i, form in enumerate(all_attested_forms):
		axis.plot(proportions[:, i], label=form)
	axis.legend(fontsize=5)
	axis.set_ylim(-0.05, 1.05)
	axis.set_ylabel('Proportion of attested spellings')
	axis.set_xticks([0, 1, 2])
	axis.set_xticklabels(BANDS)
	axis.set_xlim(-0.25, 2.25)
	plt.show()

def plot_spelling_stack(meaning):
	attested_forms_by_band = lemma_map[meaning]
	all_attested_forms = []
	for band, forms in attested_forms_by_band.items():
		all_attested_forms.extend(forms)
	all_attested_forms = list(set(all_attested_forms))
	all_attested_forms.sort()
	stack = np.zeros((len(all_attested_forms), len(BANDS)), dtype=float)
	for i, form in enumerate(all_attested_forms):
		for j, band in enumerate(BANDS):
			stack[i, j] = attested_forms_by_band[band].get(form, 0)
	for j in range(len(BANDS)):
		stack[:, j] /= stack[:, j].sum()
	fig, axis = plt.subplots(1, 1)
	axis.stackplot([0, 1, 2], stack)
	plt.show()

def entropy(D):
	D = np.array(list(D), dtype=float)
	D /= D.sum()
	return -sum([p * np.log2(p) for p in D if p > 0])

def jitter(X, scale=1):
	X = np.array(X, dtype=float)
	return X + (np.random.random(len(X)) - 0.5) * scale

def plot_entropy_by_band(with_at_least_n_spellings=1):
	entropy_by_band = defaultdict(list)
	for meaning in lemma_map:
		attested_forms_by_band = lemma_map[meaning]
		for band, forms in attested_forms_by_band.items():
			if len(forms) > with_at_least_n_spellings:
				H = entropy(forms.values())
				entropy_by_band[band].append(H)
	fig, axis = plt.subplots(1, 1, figsize=(10, 7))
	for x, band in enumerate(BANDS):
		Y = entropy_by_band[band]
		X = [x] * len(Y)
		axis.scatter(jitter(X, scale=0.5), Y, s=1, alpha=0.5)
		axis.set_xticks([0, 1, 2])
		axis.set_xticklabels(BANDS)
		axis.set_ylabel('Entropy (bits)')
	axis.plot([0, 1, 2], [np.mean(entropy_by_band[band]) for band in BANDS], color='black')
	
	fig.tight_layout()
	plt.show()


# plot_entropy_by_band(2)

plot_spelling_stack('little')