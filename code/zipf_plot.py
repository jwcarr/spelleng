from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import rankdata
import matplotlib.pyplot as plt

plt.rcParams.update({'font.sans-serif': 'Helvetica Neue', 'font.size': 7})

ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'

count_texts = pd.read_csv(DATA / 'count_corpus_texts.csv')
count_corpus = pd.read_csv(DATA / 'count_corpus.csv')
count_oed = pd.read_csv(DATA / 'count_oed.csv')



def freq_by_rank_plot(axis, freqs, title, color, label):
	freqs = freqs[ np.where(freqs > 0) ]
	sorted_freqs = sorted(freqs, reverse=True)
	axis.plot(range(1, len(sorted_freqs) + 1), sorted_freqs, color=color, label=label)
	axis.set_xscale('log')
	axis.set_yscale('log')
	axis.set_ylim(1, 100000)
	axis.set_xlim(1, 10000)
	axis.set_yticks([1, 10, 100, 1000, 10000, 100000])
	axis.set_xticks([1, 10, 100, 1000, 10000, 100000])
	axis.set_title(title, fontsize=7)
	axis.set_xlabel('Rank')



fig, axes = plt.subplots(1, 4, figsize=(7.48, 1.8), sharey=True, sharex=True)

BROAD_BANDS = {'OE': 'Old English', 'ME': 'Middle English', 'eME': 'Early Modern English', 'lME': 'Late Modern English'}

for band, axis in zip(BROAD_BANDS, axes):

	oed_totals = count_oed.groupby('lemma')[band].sum().to_numpy()
	corpus_totals = count_corpus.groupby('lemma')[band].sum().to_numpy()
	text_totals = count_texts.groupby('lemma')[band].sum().to_numpy()

	freq_by_rank_plot(axis, oed_totals, BROAD_BANDS[band], 'cadetblue', 'N quotes')
	freq_by_rank_plot(axis, text_totals, BROAD_BANDS[band], 'darkorange', 'N texts')
	freq_by_rank_plot(axis, corpus_totals, BROAD_BANDS[band], 'crimson', 'N occurrences')
	

axes[0].set_ylabel('Frequency')
axes[0].legend(frameon=False, markerfirst=False)

fig.tight_layout(pad=0.5, h_pad=0.5, w_pad=0.5)
fig.savefig(ROOT / 'manuscript' / 'figs' / 'zipf_plots.pdf')
