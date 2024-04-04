from pathlib import Path
from utils import json_read, json_write
import pandas as pd
import numpy as np


ROOT = Path(__file__).parent.parent.resolve()

BANDS = [
	'Old English (I & II)',
	'Old English (III)',
	'Old English (IV)',
	'Middle English (I)',
	'Middle English (II)',
	'Middle English (III)',
	'Middle English (IV)',
	'Early Modern English (I)',
	'Early Modern English (II)',
	'Early Modern English (III)',
	'Late Modern English (I)',
	'Late Modern English (II)',
	'Late Modern English (III)',
]


def count_variants(word_freqs, variants, pos):
	variants_untagged = [f'{v}_' for v in variants]
	variants_tagged = [f'{v}_{pos}' for v in variants]
	counts = np.zeros((len(variants), len(BANDS)), dtype=int)
	for j, band in enumerate(BANDS):
		if band.startswith('Late Modern English'):
			variants = variants_tagged
		else:
			variants = variants_untagged
		for i, variant in enumerate(variants):
			counts[i, j] = word_freqs[band].get(variant, 0)
	print(counts)


if __name__ == '__main__':

	word_freqs = json_read(ROOT / 'data' / 'word_freqs.json')

	variants = ['cing', 'cyng', 'cyning', 'king', 'kinge', 'kyng', 'kynge', 'kyning']

	count_variants(word_freqs, variants, pos='nn')
