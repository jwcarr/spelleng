from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

plt.rcParams.update({'font.sans-serif': 'Helvetica Neue', 'font.size': 7})

ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'

BROAD_BANDS = {'OE': 'Old English', 'ME': 'Middle English', 'eME': 'Early Modern English', 'lME': 'Late Modern English'}


def entropy(freq_dist):
	freq_dist = np.array(freq_dist)
	if freq_dist.sum() == 0:
		return 0
	P = freq_dist / freq_dist.sum()
	return -sum([p * np.log2(p) for p in P if p > 0])


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


count_quot = pd.read_csv(DATA / 'count_quot.csv')
count_text = pd.read_csv(DATA / 'count_text.csv')
count_freq = pd.read_csv(DATA / 'count_freq.csv')


fig = plt.figure(figsize=(7.48, 4))

grid = gridspec.GridSpec(2, 4, figure=fig)
grid_freq = gridspec.GridSpecFromSubplotSpec(1, 4, subplot_spec=grid[0, :])
grid_entr = gridspec.GridSpecFromSubplotSpec(1, 1, subplot_spec=grid[1, :])

for j, band in enumerate(BROAD_BANDS):

	axis = fig.add_subplot(grid_freq[0, j])

	quot_totals = count_quot.groupby('lemma')[band].sum().to_numpy()
	text_totals = count_text.groupby('lemma')[band].sum().to_numpy()
	freq_totals = count_freq.groupby('lemma')[band].sum().to_numpy()

	freq_by_rank_plot(axis, quot_totals, BROAD_BANDS[band], 'cadetblue', 'N quotes')
	freq_by_rank_plot(axis, text_totals, BROAD_BANDS[band], 'darkorange', 'N texts')
	freq_by_rank_plot(axis, freq_totals, BROAD_BANDS[band], 'crimson', 'N occurrences')
	
	if j == 0:
		axis.set_ylabel('Lemma frequency')
	else:
		axis.set_yticklabels([])


axis = fig.add_subplot(grid_entr[0, 0])

quot_entropy_by_band = []
text_entropy_by_band = []
freq_entropy_by_band = []

for band_i in range(1, 14):
	band_header = f'band_{band_i}'
	print(band_header)
	quot_entropy_by_band.append(
		count_quot.groupby('lemma')[band_header].apply(lambda x: entropy(x)).to_numpy().mean()
	)
	text_entropy_by_band.append(
		count_text.groupby('lemma')[band_header].apply(lambda x: entropy(x)).to_numpy().mean()
	)
	freq_entropy_by_band.append(
		count_freq.groupby('lemma')[band_header].apply(lambda x: entropy(x)).to_numpy().mean()
	)

axis.plot(range(1, 14), quot_entropy_by_band, '-o', color='cadetblue', label='N OED quotations')
axis.plot(range(1, 14), text_entropy_by_band, '-o', color='darkorange', label='N corpus texts')
axis.plot(range(1, 14), freq_entropy_by_band, '-o', color='crimson', label='N corpus occurrences')

# axis.plot(range(1, 14), range(1, 14), '-o', color='cadetblue', label='N OED quotations')
# axis.plot(range(1, 14), range(1, 14), '-o', color='darkorange', label='N corpus texts')
# axis.plot(range(1, 14), range(1, 14), '-o', color='crimson', label='N corpus occurrences')

axis.set_xlabel('Historical band')
axis.set_ylabel('Mean variant entropy (bits)')

axis.set_xticks(list(range(1, 14)))
axis.set_xticklabels(list(range(1, 14)))
axis.set_xlim(0.5, 13.5)

axis.axvline(3.5, color='gray', linewidth=0.5, linestyle='--')
axis.axvline(7.5, color='gray', linewidth=0.5, linestyle='--')
axis.axvline(10.5, color='gray', linewidth=0.5, linestyle='--')

axis.legend(frameon=False, markerfirst=False)


fig.tight_layout(pad=0.5, h_pad=1.0, w_pad=2.0)
fig.savefig(ROOT / 'manuscript' / 'figs' / 'entropy_plot.pdf')
