from collections import defaultdict
from pathlib import Path
import utils
import numpy as np
import pandas as pd


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'
OED_QUOTATIONS = DATA / 'oed_quotations'

CLMET_POS_MAP = {'n': 'nn', 'v': 'vb', 'adj': 'jj'}

BANDS = [
	( 800,  950, "Old English (I & II)"),
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

BROAD_BANDS = {'OE': [1, 2, 3, 4], 'ME': [5, 6, 7], 'eME': [8, 9, 10], 'lME': [11, 12, 13]}


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

def add_broad_band_counts(dataset):
	for broad_band, narrow_bands in BROAD_BANDS.items():
		columns = [f'band_{band_i}' for band_i in narrow_bands]
		dataset[broad_band] = dataset[columns].sum(axis=1)
	dataset['total'] = dataset[ list(BROAD_BANDS.keys()) ].sum(axis=1)

def count_quotations(lemma, variants, quotation_data):
	counts = np.zeros((len(variants), len(BANDS)), dtype=int)
	for variant_i, variant in enumerate(variants):
		for year, quote in quotation_data[variant]['quotations']:
			band_i = determine_band(year)
			if band_i is None:
				continue
			counts[variant_i, band_i] += 1
	return counts

def count_corpus(lemma, variants, quotation_data, corpus):
	pos = CLMET_POS_MAP[ lemma.split('_')[1] ]
	variants_untagged = [f'{v}_' for v in variants]
	variants_tagged = [f'{v}_{pos}' for v in variants]
	counts_texts = np.zeros((len(variants), len(BANDS)), dtype=int)
	counts_freqs = np.zeros((len(variants), len(BANDS)), dtype=int)
	for band_i, (s, e, band) in enumerate(BANDS):
		search_variants = variants_tagged if band.startswith('Late Modern English') else variants_untagged
		for variant_i, (variant, search_variant) in enumerate(zip(variants, search_variants)):
			start = quotation_data[variant]['start']
			end = quotation_data[variant]['end']
			for document in corpus[band]:
				if document['year'] >= start and document['year'] <= end:
					if search_variant in document['freqs']:
						counts_texts[variant_i, band_i] += 1
						counts_freqs[variant_i, band_i] += document['freqs'][search_variant]
	return counts_texts, counts_freqs

def add_counts_to_corpus(corpus):
	for band, documents in corpus.items():
		for document in documents:
			document['freqs'] = defaultdict(int)
			for token in document['text'].split(' '):
				document['freqs'][token] += 1


if __name__ == '__main__':

	lemmata = utils.json_read(DATA / 'lemmata.json')
	lemmata = sorted(list(lemmata.keys()))

	corpus = utils.json_read(DATA / 'corpus.json')
	add_counts_to_corpus(corpus)

	quot_data_frames = []
	text_data_frames = []
	freq_data_frames = []
	for lemma_i, lemma in enumerate(lemmata):
		if lemma_i % 100 == 0:
			print(lemma_i, lemma)

		quotation_data_path = OED_QUOTATIONS / f'{lemma}.json'
		if not quotation_data_path.exists():
			continue

		quotation_data = utils.json_read(quotation_data_path)
		variants = sorted(list(quotation_data.keys()))
		
		quot_count = count_quotations(lemma, variants, quotation_data)
		text_count, freq_count = count_corpus(lemma, variants, quotation_data, corpus)

		variants_to_keep = np.where( (quot_count + text_count).sum(axis=1) > 0 )[0]
		final_variants = [variant for variant_i, variant in enumerate(variants)	 if variant_i in variants_to_keep]

		quot_data_frames.append(
			create_dataframe(lemma, final_variants, quot_count[variants_to_keep, :])
		)
		text_data_frames.append(
			create_dataframe(lemma, final_variants, text_count[variants_to_keep, :])
		)
		freq_data_frames.append(
			create_dataframe(lemma, final_variants, freq_count[variants_to_keep, :])
		)

	quotation_dataset = pd.concat(quot_data_frames, ignore_index=True)
	add_broad_band_counts(quotation_dataset)
	quotation_dataset.to_csv(DATA / 'count_quot.csv', index=False)

	corpus_dataset = pd.concat(text_data_frames, ignore_index=True)
	add_broad_band_counts(corpus_dataset)
	corpus_dataset.to_csv(DATA / 'count_text.csv', index=False)

	corpus_dataset = pd.concat(freq_data_frames, ignore_index=True)
	add_broad_band_counts(corpus_dataset)
	corpus_dataset.to_csv(DATA / 'count_freq.csv', index=False)
