from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, gaussian_kde
import matplotlib.pyplot as plt


plt.rcParams.update({'font.sans-serif': 'Helvetica Neue', 'font.size': 7})


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'
SPELLENG = ROOT / 'spelleng'


def correlate(counts1, counts2):
	nonzero = np.where( (counts1 + counts2) > 0 )[0]
	counts1 = counts1[nonzero]
	counts2 = counts2[nonzero]
	if len(counts1) < 2:
		return None
	if len(np.unique(counts1)) < 2 or len(np.unique(counts2)) < 2:
		return None
	return spearmanr(counts1, counts2)[0]

def calculate_correlation_per_band(counts1, counts2):
	correlations = []
	for band_i in range(1, 14):
		band_id = f'band{band_i}'
		r = correlate(counts1[band_id].to_numpy(), counts2[band_id].to_numpy())
		if r is None:
			continue
		correlations.append(r)
	return correlations

def calculate_distribution(counts1, counts2):
	correlations = []
	for i, (lemma_id, subset) in enumerate(counts1):
		if i % 1000 == 0:
			print(i)
		correlations.extend(
			calculate_correlation_per_band(subset, counts2.get_group(lemma_id))
		)
		# if i == 1000:
		# 	break
	return correlations

def plot_distribution(distribution):
	print(len(distribution))
	fig, axis = plt.subplots(1, 1, figsize=(3.54, 2))
	x = np.linspace(-1, 1, 50)
	y = gaussian_kde(distribution).pdf(x)
	axis.plot(x, y, color='black')
	axis.set_xlim(-1, 1)
	axis.set_ylim(0, axis.get_ylim()[1])
	axis.set_yticks([])
	# axis.set_yticklabels([])
	axis.set_xlabel("Spearman's ρ")
	axis.set_ylabel("Density")
	fig.tight_layout()
	plt.show()


if __name__ == '__main__':

	counts_quot = pd.read_csv(SPELLENG / 'spelleng_quote.csv')
	counts_text = pd.read_csv(SPELLENG / 'spelleng_text.csv')
	# counts_freq = pd.read_csv(SPELLENG / 'spelleng_token.csv')

	distribution = calculate_distribution(counts_quot.groupby('lemma_id'), counts_text.groupby('lemma_id'))
	plot_distribution(distribution)