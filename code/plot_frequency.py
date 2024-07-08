from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

plt.rcParams.update({'font.sans-serif': 'Helvetica Neue', 'font.size': 7})

ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'

BROAD_BANDS = {'OE': 'Old English', 'ME': 'Middle English', 'eME': 'Early Modern English', 'lME': 'Late Modern English'}

BAND_LABELS = [
	"Band 1\nPre-950",
	"Band 2\n950–1049",
	"Band 3\n1050–1149",
	"Band 4\n1150–1249",
	"Band 5\n1250–1349",
	"Band 6\n1350–1419",
	"Band 7\n1420–1499",
	"Band 8\n1500–1569",
	"Band 9\n1570–1639",
	"Band 10\n1640–1709",
	"Band 11\n1710–1779",
	"Band 12\n1780–1849",
	"Band 13\n1850–1919",
]


def entropy(freq_dist):
	freq_dist = np.array(freq_dist)
	if freq_dist.sum() == 0:
		return None
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

count_quot = pd.read_csv(ROOT / 'spelleng' / 'spelleng_quote.csv')
count_text = pd.read_csv(ROOT / 'spelleng' / 'spelleng_text.csv')
count_freq = pd.read_csv(ROOT / 'spelleng' / 'spelleng_token.csv')


fig = plt.figure(figsize=(7.48, 4.9))

grid = gridspec.GridSpec(3, 4, figure=fig)
grid_freq = gridspec.GridSpecFromSubplotSpec(1, 4, subplot_spec=grid[0, :])
grid_nvar = gridspec.GridSpecFromSubplotSpec(1, 4, subplot_spec=grid[1, :])
grid_entr = gridspec.GridSpecFromSubplotSpec(1, 1, subplot_spec=grid[2, :])

for j, band in enumerate(BROAD_BANDS):

	axis = fig.add_subplot(grid_freq[0, j])

	quot_totals = count_quot.groupby('lemma_id')[band].sum().to_numpy()
	text_totals = count_text.groupby('lemma_id')[band].sum().to_numpy()
	freq_totals = count_freq.groupby('lemma_id')[band].sum().to_numpy()

	freq_by_rank_plot(axis, quot_totals, BROAD_BANDS[band], 'cadetblue', 'quotation count')
	freq_by_rank_plot(axis, text_totals, BROAD_BANDS[band], 'darkorange', 'text count')
	freq_by_rank_plot(axis, freq_totals, BROAD_BANDS[band], 'crimson', 'token count')
	
	if j == 0:
		axis.set_ylabel('Lemma frequency')
		axis.legend(frameon=False, markerfirst=False)
	else:
		axis.set_yticklabels([])


	axis = fig.add_subplot(grid_nvar[0, j])

	combined_count = count_quot + count_text
	quot_nvars = combined_count[ combined_count[band] > 0 ].groupby('lemma_id')[band].count().to_list()
	n_lemmata_quot = len(combined_count[ combined_count[band] > 0 ]['lemma_id'].unique())
	n_variants_plot(axis, quot_nvars, 'black', n_lemmata_quot)

	if j == 0:
		axis.set_ylabel('Proportion of lemmata')
	else:
		axis.set_yticklabels([])
	if j == 3:
		axis.legend(frameon=False, markerfirst=False)


axis = fig.add_subplot(grid_entr[0, 0])

quot_entropy_by_band = []
text_entropy_by_band = []
freq_entropy_by_band = []

for band_i in range(1, 14):
	band_header = f'band{band_i}'
	print(band_header)
	quot_entropy_by_band.append(
		count_quot.groupby('lemma_id')[band_header].apply(lambda x: entropy(x)).mean()
	)
	text_entropy_by_band.append(
		count_text.groupby('lemma_id')[band_header].apply(lambda x: entropy(x)).mean()
	)
	freq_entropy_by_band.append(
		count_freq.groupby('lemma_id')[band_header].apply(lambda x: entropy(x)).mean()
	)

axis.plot(range(1, 14), quot_entropy_by_band, '-o', color='cadetblue', label='$N$ OED quotations')
axis.plot(range(1, 14), text_entropy_by_band, '-o', color='darkorange', label='$N$ corpus texts')
axis.plot(range(1, 14), freq_entropy_by_band, '-o', color='crimson', label='$N$ corpus tokens')

# axis.plot(range(1, 14), range(1, 14), '-o', color='cadetblue', label='N OED quotations')
# axis.plot(range(1, 14), range(1, 14), '-o', color='darkorange', label='N corpus texts')
# axis.plot(range(1, 14), range(1, 14), '-o', color='crimson', label='N corpus occurrences')

# axis.set_xlabel('Historical band')
axis.set_ylabel('Mean variant entropy (bits)')

axis.set_xticks(list(range(1, 14)))
axis.set_xticklabels(BAND_LABELS)
axis.set_xlim(0.5, 13.5)
axis.set_ylim(0, 1)

axis.axvline(3.5, color='gray', linewidth=0.5, linestyle='--')
axis.axvline(7.5, color='gray', linewidth=0.5, linestyle='--')
axis.axvline(10.5, color='gray', linewidth=0.5, linestyle='--')

# axis.legend(frameon=False, markerfirst=False)

fig.tight_layout(pad=0.5, h_pad=1.0, w_pad=2.0)
fig.savefig(ROOT / 'manuscript' / 'figs' / 'frequency_plot.pdf')
