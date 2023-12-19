from pathlib import Path
from utils import json_read, json_write
import pandas as pd


ROOT = Path(__file__).parent.parent.resolve()


BROAD_BANDS = [
	( 800, 1150, 'Old English'),
	(1150, 1500, 'Middle English'),
	(1500, 1710, 'Early Modern English'),
	(1710, 2000, 'Late Modern English'),
]

NARROW_BANDS = [
	( 800,  850, "Old English (I)"),
	( 850,  950, "Old English (II)"),
	( 950, 1050, "Old English (III)"),
	(1050, 1150, "Old English (IV)"),
	(1150, 1250, "Middle English (I)"),
	(1250, 1350, "Middle English (II)"),
	(1350, 1420, "Middle English (III)"),
	(1420, 1500, "Middle English (IV)"),
	(1500, 1570, "Early Modern English (I)"),
	(1570, 1640, "Early Modern English (II)"),
	(1640, 1710, "Early Modern English (III)"),
	(1710, 1800, "Late Modern English (I)"),
	(1800, 1900, "Late Modern English (II)"),
	(1900, 2000, "Late Modern English (III)"),
]


def classify_band(year, classification_bands):
	for start, end, band in classification_bands:
		if year >= start and year < end:
			return band
	return None

def classify_into_bands(lemma_quotation_data, classification_bands):
	variant_counts_by_band = {}
	for variant, quotations in lemma_quotation_data.items():
		band_counts = {band: 0 for s, e, band in classification_bands}
		for year, quote in quotations:
			if band := classify_band(year, classification_bands):
				band_counts[band] += 1
		variant_counts_by_band[variant] = band_counts
	return variant_counts_by_band

def make_table(variant_counts_by_band, classification_bands):
	table = []
	for variant, counts_by_band in variant_counts_by_band.items():
		counts = [counts_by_band[band] for s, e, band in classification_bands]
		if sum(counts) > 0:
			table.append(
				[variant] + counts
			)
	table = pd.DataFrame(table)#, columns=['variant', 'OE', 'ME', 'EME', 'LME'])
	return table


def output(counts, classification_bands):
	for lemma, variant_counts_by_band in counts.items():
		table = make_table(variant_counts_by_band, classification_bands)
		print(lemma)
		print(table)
		print('')


if __name__ == '__main__':

	lemmata_file = ROOT / 'data' / 'lemmata.txt'

	with open(lemmata_file) as file:
		lemmata = file.read()
	lemmata = lemmata.split('\n')

	counts = {}
	for lemma in lemmata:
		lemma_json_path = ROOT / 'data' / 'oed' / f'{lemma}.json'
		lemma_quotation_data = json_read(lemma_json_path)
		counts[lemma] = classify_into_bands(lemma_quotation_data, BROAD_BANDS)

	json_write(counts, ROOT / 'data' / 'oed_variant_counts.json')

	output(counts, BROAD_BANDS)
