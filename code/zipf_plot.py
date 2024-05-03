from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import rankdata
import matplotlib.pyplot as plt

ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'

count_corpus = pd.read_csv(DATA / 'count_corpus_texts.csv')
count_oed = pd.read_csv(DATA / 'count_oed.csv')


fig, axes = plt.subplots(3, 5, figsize=(5, 3), sharey=True)
axes = axes.flatten()

for band_i in range(1, 14):

	axis = axes[band_i - 1]

	corpus_totals = count_corpus.groupby('lemma')[f'band_{band_i}'].sum().to_numpy()
	oed_totals = count_oed.groupby('lemma')[f'band_{band_i}'].sum().to_numpy()

	lemma = count_oed['lemma'].unique()

	oed_ranks = rankdata(-(oed_totals + corpus_totals), method='ordinal')

	oed_means = []
	cor_means = []

	for i in range(0, len(oed_ranks), 100):
		indices_in_rank_band = np.where((oed_ranks >= i) & (oed_ranks < (i + 100)))
		oed_means.append(oed_totals[indices_in_rank_band].mean())
		cor_means.append(corpus_totals[indices_in_rank_band].mean())

	end_rank_index = oed_means.index(0)

	x = [i * 100 + 1 for i, _ in enumerate(oed_means[:end_rank_index])]

	axis.plot(x, oed_means[:end_rank_index], color='cadetblue')
	axis.plot(x, cor_means[:end_rank_index], color='crimson')

	# axis.set_xscale('log')
	axis.set_yscale('log')

axes[13].axis('off')
axes[14].axis('off')

fig.tight_layout(pad=0.1, h_pad=0.1, w_pad=0.1)

plt.show()
