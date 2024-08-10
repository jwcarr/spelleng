from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams.update({'font.sans-serif': 'Helvetica Neue', 'font.size': 7})


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'

BROAD_BANDS = {'oe': 'Old English', 'me': 'Middle English', 'eme': 'Early Modern English', 'lme': 'Late Modern English'}


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
	axis.set_xlabel('Lemma rank')

def n_variants_plot(axis, number_of_variants, color, n, greater_than=8):
	n_vars = [number_of_variants.count(i) / n for i in range(1, greater_than+1)]
	n_vars = n_vars + [1 - sum(n_vars)]
	axis.axvline(np.mean(number_of_variants), color='gray', label='mean', linestyle=':', linewidth=1)
	axis.axvline(np.median(number_of_variants), color='mediumseagreen', label='median', linestyle=':', linewidth=1)
	axis.bar(np.arange(1, greater_than+2), n_vars, color=color)
	axis.set_xlim(0, greater_than+2)
	axis.set_ylim(0, 1)
	axis.set_xlabel('Number of variants')
	axis.set_xticks(list(range(1, greater_than+2)))
	axis.set_xticklabels(list(range(1, greater_than+1)) + [f'>{greater_than}'])

def plot_frequency(output_file):

	fig, axes = plt.subplots(2, 4, figsize=(7.48, 3.3))

	for j, band in enumerate(BROAD_BANDS):

		axis = axes[0, j]

		quot_totals = count_quot.groupby('lemma')[band].sum().to_numpy()
		text_totals = count_text.groupby('lemma')[band].sum().to_numpy()
		freq_totals = count_freq.groupby('lemma')[band].sum().to_numpy()

		freq_by_rank_plot(axis, quot_totals, BROAD_BANDS[band], 'cadetblue', 'quotation count')
		freq_by_rank_plot(axis, text_totals, BROAD_BANDS[band], 'darkorange', 'text count')
		freq_by_rank_plot(axis, freq_totals, BROAD_BANDS[band], 'crimson', 'token count')
		
		if j == 0:
			axis.set_ylabel('Lemma frequency')
			axis.legend(frameon=False, markerfirst=False)
		else:
			axis.set_yticklabels([])

		axis = axes[1, j]

		combined_count = count_quot + count_text
		quot_nvars = combined_count[ combined_count[band] > 0 ].groupby('lemma')[band].count().to_list()
		n_lemmata_quot = len(combined_count[ combined_count[band] > 0 ]['lemma'].unique())
		n_variants_plot(axis, quot_nvars, 'black', n_lemmata_quot)

		if j == 0:
			axis.set_ylabel('Proportion of lemmata')
		else:
			axis.set_yticklabels([])
		if j == 3:
			axis.legend(frameon=False, markerfirst=False)

	fig.tight_layout(pad=0.5, h_pad=0.5, w_pad=0.5)
	fig.savefig(output_file)


if __name__ == '__main__':

	count_quot = pd.read_csv(DATA / 'spelleng_quote.csv')
	count_text = pd.read_csv(DATA / 'spelleng_text.csv')
	count_freq = pd.read_csv(DATA / 'spelleng_token.csv')

	plot_frequency(ROOT / 'manuscript' / 'figs' / 'frequency_plot.pdf')
