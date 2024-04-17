from pathlib import Path
import utils
import numpy as np
import pandas as pd


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'
OED_QUOTATIONS = DATA / 'oed_quotations'

CLMET_POS_MAP = {'n': 'nn', 'v': 'vb', 'adj': 'jj'}

BANDS = [
	(   0,  950, "Old English (I & II)"),
	( 950, 1050, "Old English (III)"),
	(1050, 1150, "Old English (IV)"),
	(1150, 1250, "Middle English (I)"),
	(1250, 1350, "Middle English (II)"),
	(1350, 1420, "Middle English (III)"),
	(1420, 1500, "Middle English (IV)"),
	(1500, 1570, "Early Modern English (I)"),
	(1570, 1640, "Early Modern English (II)"),
	(1640, 1710, "Early Modern English (III)"),
	(1710, 1780, "Late Modern English (I)"),
	(1780, 1850, "Late Modern English (II)"),
	(1850, 1920, "Late Modern English (III)"),
]


def determine_band(year):
	for band_i, (start, end, band_name) in enumerate(BANDS):
		if year >= start and year < end:
			return band_i
	return None

def create_dataframe(lemma, variants, counts):
	data = {
		'lemma': [lemma] * len(variants),
		'variant': variants,
	}
	data.update(
		{f'band_{i + 1}': counts[:, i] for i in range(len(BANDS))}
	)
	return pd.DataFrame(data)

def count_quotations(lemma, variants, quotation_data):
	counts = np.zeros((len(variants), len(BANDS)), dtype=int)
	for variant_i, variant in enumerate(variants):
		for year, quote in quotation_data[variant]['quotations']:
			band_i = determine_band(year)
			if band_i is None:
				continue
			counts[variant_i, band_i] += 1
	return counts

def count_corpus(lemma, variants, quotation_data, word_freqs):
	pos = CLMET_POS_MAP[ lemma.split('_')[1] ]
	variants_untagged = [f'{v}_' for v in variants]
	variants_tagged = [f'{v}_{pos}' for v in variants]
	counts = np.zeros((len(variants), len(BANDS)), dtype=int)
	for band_i, (s, e, band) in enumerate(BANDS):
		search_variants = variants_tagged if band.startswith('Late Modern English') else variants_untagged
		for variant_i, (variant, search_variant) in enumerate(zip(variants, search_variants)):
			start = quotation_data[variant]['start']
			end = quotation_data[variant]['end']
			if s < start or e > end:
				continue
			counts[variant_i, band_i] = word_freqs[band].get(search_variant, 0)
	return counts


if __name__ == '__main__':

	word_freqs = utils.json_read(DATA / 'word_freqs.json')

	lemmata = utils.json_read(DATA / 'lemmata.json')
	lemmata = sorted(list(lemmata.keys()))

	quotation_data_frames = []
	corpus_data_frames = []
	for lemma_i, lemma in enumerate(lemmata):
		if lemma_i % 100 == 0:
			print(lemma_i, lemma)

		quotation_data_path = OED_QUOTATIONS / f'{lemma}.json'
		if not quotation_data_path.exists():
			continue

		quotation_data = utils.json_read(quotation_data_path)
		variants = sorted(list(quotation_data.keys()))
		
		quote_count = count_quotations(lemma, variants, quotation_data)
		corpus_count = count_corpus(lemma, variants, quotation_data, word_freqs)
		combined_count = quote_count + corpus_count

		variants_to_keep = np.where(combined_count.sum(axis=1) > 0)[0]
		final_variants = [variant for variant_i, variant in enumerate(variants)	 if variant_i in variants_to_keep]

		quotation_data_frames.append(
			create_dataframe(lemma, final_variants, quote_count[variants_to_keep, :])
		)
		corpus_data_frames.append(
			create_dataframe(lemma, final_variants, corpus_count[variants_to_keep, :])
		)

	quotation_dataset = pd.concat(quotation_data_frames, ignore_index=True)
	quotation_dataset.to_csv(DATA / 'count_oed.csv', index=False)

	corpus_dataset = pd.concat(corpus_data_frames, ignore_index=True)
	corpus_dataset.to_csv(DATA / 'count_corpus.csv', index=False)
