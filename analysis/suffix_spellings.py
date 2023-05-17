from collections import defaultdict
from pathlib import Path
from utils import json_read, json_write
import numpy as np
import matplotlib.pyplot as plt


ROOT = Path(__file__).parent.parent.resolve()

BANDS = ['Old English', 'Middle English', 'Early Modern English']

oed_suffix_forms = {
	'ness': ['nace', 'nas', 'nase', 'nasse', 'nece', 'nes', 'nesce', 'nesch', 'nese', 'ness', 'nessche', 'nesse', 'nesshe', 'nez', 'nis', 'nise', 'niss', 'nisse', 'nus', 'nuss', 'nys', 'nyss', 'nysse', 'næs'],
	'ful':  ['fa', 'ffol', 'fful', 'ffull', 'fil', 'fol', 'fole', 'folle', 'foo', 'fou', 'foul', 'foull', 'fow', 'fu', 'ful', 'fule', 'full', 'fulle', 'fwll', 'uel', 'uol', 'uull', 'vul'],
	'ous':  ['es', 'is', 'ois', 'os', 'ose', 'ous', 'ouse', 'ows', 'owse', 'us', 'ys'],
	'ic':   ['ic', 'ick', 'ik', 'ike', 'ique', 'icke', 'ycke', 'eck', 'yk', 'yke'],
	'al':   ['ale', 'alle', 'ell', 'el', 'al', 'all'],
	'ship': ['chep', 'chepe', 'chipe', 'chyp', 'scep', 'schepe', 'schip', 'schipe', 'schippe', 'schupe', 'schuppe', 'schyp', 'sciop', 'scip', 'scipe', 'scype', 'shep', 'ship', 'shipe', 'shipp', 'shippe', 'shyp', 'shyppe', 'sip', 'skiepe'],
	'less': ['las', 'lase', 'leas', 'lease', 'lees', 'les', 'lese', 'less', 'lesse', 'lez', 'leæs', 'lias', 'lies', 'liese', 'lis', 'lyas', 'læs'],
}

lemma_map = json_read(ROOT / 'data' / 'lemma_map.json')


def plot_spelling_stack(stack, forms):
	reduced_stack = []
	reduced_forms = []
	for row, form in zip(stack, forms):
		if row.sum() > 0:
			reduced_stack.append(row)
			reduced_forms.append(form)
	reduced_stack = np.array(reduced_stack)
	for j in range(len(BANDS)):
		reduced_stack[:, j] /= reduced_stack[:, j].sum()
	fig, axis = plt.subplots(1, 1)
	axis.stackplot([0, 1, 2], reduced_stack, labels=reduced_forms)
	axis.legend(fontsize=8)
	axis.set_ylim(0, 1)
	axis.set_ylabel('Proportion of attested spellings')
	axis.set_xticks([0, 1, 2])
	axis.set_xticklabels(BANDS)
	axis.set_xlim(0, 2)
	plt.show()

def count_spellings_of_suffix(suffix):
	suffixed_lemmas = {}
	for lemma, data in lemma_map.items():
		if lemma.endswith(suffix):
			suffixed_lemmas[lemma] = data
	suffix_forms = sorted(oed_suffix_forms[suffix], key=lambda f: len(f), reverse=True)
	counts = np.zeros((len(suffix_forms), len(BANDS)), dtype=float)
	for lemma, data in suffixed_lemmas.items():
		for band, forms in data.items():
			j = BANDS.index(band)
			for form, count in forms.items():
				for i, suffix_form in enumerate(suffix_forms):
					if form.endswith(suffix_form):
						counts[i, j] += count
						break
				else:
					print('Cannot map', form)
	return counts, suffix_forms


counts, suffix_forms = count_spellings_of_suffix('less')
plot_spelling_stack(counts, suffix_forms)
