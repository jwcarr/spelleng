from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams.update({'font.sans-serif': 'Helvetica Neue', 'font.size': 7})


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'

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

def plot_entropy(output_file):

	fig, axis = plt.subplots(1, 1, figsize=(7.48, 2))

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

	axis.plot(range(1, 14), quot_entropy_by_band, '-o', color='cadetblue', label='quotation count')
	axis.plot(range(1, 14), text_entropy_by_band, '-o', color='darkorange', label='text count')
	axis.plot(range(1, 14), freq_entropy_by_band, '-o', color='crimson', label='token count')

	axis.set_ylabel('Mean variant entropy (bits)')

	axis.set_xticks(list(range(1, 14)))
	axis.set_xticklabels(BAND_LABELS)
	axis.set_xlim(0.5, 13.5)
	axis.set_ylim(0, 1)

	axis.axvline(3.5, color='gray', linewidth=0.5, linestyle='--')
	axis.axvline(7.5, color='gray', linewidth=0.5, linestyle='--')
	axis.axvline(10.5, color='gray', linewidth=0.5, linestyle='--')

	axis.legend(frameon=False, markerfirst=False)

	fig.tight_layout(pad=0.5, h_pad=1.0, w_pad=2.0)
	fig.savefig(output_file)


if __name__ == '__main__':

	count_quot = pd.read_csv(DATA / 'spelleng_quote.csv')
	count_text = pd.read_csv(DATA / 'spelleng_text.csv')
	count_freq = pd.read_csv(DATA / 'spelleng_token.csv')

	plot_entropy(ROOT / 'manuscript' / 'figs' / 'entropy_plot.pdf')
