from utils import json_read, json_write
import numpy as np

lexemes = ["man", "god", "king", "lord", "father", "Christ", "place", "Jesus", "brother", "world", "house", "child", "woman", "body", "water", "time", "work", "folk", "word", "grace", "name", "bishop", "wife", "life", "son", "earth", "daughter", "London", "matter", "lady", "master", "hand", "knight", "love", "church", "night", "heart", "mercy", "duke", "power"]

NARROW_BANDS = [
	'Old English (I)', 'Old English (II)', 'Old English (III)', 'Old English (IV)',
	'Middle English (I)', 'Middle English (II)', 'Middle English (III)', 'Middle English (IV)',
	'Early Modern English (I)', 'Early Modern English (II)', 'Early Modern English (III)'
]

data = json_read('../data/lemma_map_subbanded.json')

dataset = {}

for lexeme in lexemes:

	variants = []
	for band in NARROW_BANDS:
		variants.extend(data[lexeme][band].keys())
	variants = sorted(list(set(variants)))

	freq_dist = np.zeros((len(NARROW_BANDS), len(variants)), dtype=int)
	for i, band in enumerate(NARROW_BANDS):
		for j, variant in enumerate(variants):
			freq_dist[i,j] = data[lexeme][band].get(variant, 0)

	dataset[lexeme] = {
		'variants': variants,
		'freq_dist': freq_dist.tolist(),
	}

json_write(dataset, '../data/freq_dist.json')
