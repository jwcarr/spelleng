from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'

count_cor = pd.read_csv(DATA / 'count_corpus_freqs.csv')
count_oed = pd.read_csv(DATA / 'count_oed.csv')


count_oed_g = count_oed.groupby('lemma')
count_cor_g = count_cor.groupby('lemma')



def determine_dominant_form(counts, variants):
	if counts.sum() == 0:
		return None # lemma is unattested in this band
	mx = counts.max()
	return [variants[i] for i in np.where(counts == mx)[0]]

def agree(variants1, variants2):
	if variants1 is None and variants2 is None:
		return True
	if variants1 is None or variants2 is None:
		return False
	variants1, variants2 = sorted([variants1, variants2], key=lambda l: len(l))
	if set(variants1).issubset(set(variants2)):
		return True
	return False


# a = determine_dominant_form(np.array([1, 0, 0, 0]), ['a', 'b', 'c', 'd'])
# b = determine_dominant_form(np.array([0, 0, 0, 0]), ['a', 'b', 'c', 'd'])

# print(a, b)

# print(agree(a, b))


# quit()


agreements = []

for i, lemma in enumerate(count_oed['lemma'].unique()):

	# if i % 1000 == 0:
	# 	print(i, lemma)
	

	subset_oed = count_oed_g.get_group(lemma)
	subset_cor = count_cor_g.get_group(lemma)

	n_variants = subset_oed.shape[0]
	if n_variants == 1:
		continue

	variants = list(subset_oed['variant'])

	n_in_agreement = 0

	for band_i in range(1, 14):

		band_oed = subset_oed[f'band_{band_i}'].to_numpy()
		band_cor = subset_cor[f'band_{band_i}'].to_numpy()

		oed_dom = determine_dominant_form(band_oed, variants)
		cor_dom = determine_dominant_form(band_cor, variants)

		n_in_agreement += agree(oed_dom, cor_dom)

	if n_in_agreement < 7:
		print(n_in_agreement, lemma)

	agreements.append(n_in_agreement)


plt.hist(agreements, bins=range(0, 14))
plt.show()

