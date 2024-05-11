from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams.update({'font.sans-serif': 'Helvetica Neue', 'font.size': 7})


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'


def determine_dominant_form(counts, variants):
	if counts.sum() == 0:
		return None # lemma is unattested in this band
	mx = counts.max()
	return set([variants[i] for i in np.where(counts == mx)[0]])

def agreement_on_dominant_form(variants1, variants2):
	if variants1 is None and variants2 is None:
		return True # no attested forms in both bands
	if variants1 is None or variants2 is None:
		return False # attested forms in one band but not the other
	variants1, variants2 = sorted([variants1, variants2], key=lambda l: len(l))
	if variants1.issubset(variants2):
		return True 
	return False

def calculate_agreement(counts1, counts2, variants):
	n_bands_in_agreement = 0
	for band_i in range(1, 14):
		band_counts_1 = counts1[f'band_{band_i}'].to_numpy()
		band_counts_2 = counts2[f'band_{band_i}'].to_numpy()
		dom_forms1 = determine_dominant_form(band_counts_1, variants)
		dom_forms2 = determine_dominant_form(band_counts_2, variants)
		n_bands_in_agreement += agreement_on_dominant_form(dom_forms1, dom_forms2)
	return n_bands_in_agreement

def make_agreement_figure(counts_oed, counts_cor, output_file):
	lemmata = counts_oed['lemma'].unique()
	counts_oed = counts_oed.groupby('lemma')
	counts_cor = counts_cor.groupby('lemma')
	agreements = []
	for i, lemma in enumerate(lemmata):
		if i % 1000 == 0:
			print(i, lemma)
		lemma_counts_oed = counts_oed.get_group(lemma)
		lemma_counts_cor = counts_cor.get_group(lemma)
		variants = list(lemma_counts_oed['variant'])
		agreements.append(
			calculate_agreement(lemma_counts_oed, lemma_counts_cor, variants)
		)
	histogram = [agreements.count(i) for i in range(0, 14)]
	fig, axis = plt.subplots(1, 1, figsize=(3.54, 2))
	axis.bar(range(0, 14), histogram, color='black')
	axis.set_xticks(list(range(0, 14)))
	axis.set_xticklabels(list(range(0, 14)))
	axis.set_xlabel('Agreement score')
	axis.set_ylabel('Number of lemmata')
	fig.tight_layout()
	fig.savefig(output_file)


if __name__ == '__main__':

	counts_quot = pd.read_csv(DATA / 'count_quot.csv')
	counts_text = pd.read_csv(DATA / 'count_text.csv')
	counts_freq = pd.read_csv(DATA / 'count_freq.csv')

	make_agreement_figure(counts_quot, counts_text, ROOT / 'manuscript' / 'figs' / 'agreement.pdf')
	# make_agreement_figure(counts_text, counts_freq, ROOT / 'manuscript' / 'figs' / 'agreement2.pdf')
