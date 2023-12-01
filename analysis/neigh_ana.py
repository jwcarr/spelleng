from collections import defaultdict
import re
from pathlib import Path
from utils import json_read
import Levenshtein
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import linregress

ROOT = Path(__file__).parent.parent.resolve()

plt.rcParams.update({'font.sans-serif': 'Helvetica Neue', 'font.size': 7})

WORD_REGEX = re.compile(r'[abcdefghijklmnopqrstuvwxyzæðþęłȝꝥ]+')


def normalize_text(text):
	'''
	Convert a text to lowercase and strip all non-alphabetical characters.
	'''
	return re.sub(r'[^\w\s]', '', text.lower())

def calculate_density(word_types):
	densities = []
	for word1, p in word_types.items():
		total = 0
		for word2 in word_types:
			total += Levenshtein.distance(word1, word2) / max(len(word1), len(word2))
		densities.append( (total / len(word_types)) * p )
	return sum(densities)

def reduce(dic, n=1000):
	top_n_words = sorted(dic, key=lambda w: -dic[w])[:n]
	return {word: dic[word] for word in top_n_words}

def values_to_probs(dic, weighted=True):
	total = sum(dic.values())
	for key, value in dic.items():
		if weighted:
			dic[key] = value / total
		else:
			dic[key] = 1 / len(dic)
	return dic

def lexeme_distance(lexeme, all_words_from_band):
	distances = []
	norm_distances = []
	for variant in lexeme:
		for word in all_words_from_band:
			dist = Levenshtein.distance(variant, word)
			distances.append(dist)
			norm_distances.append( dist / max(len(variant), len(word)) )
	return sum(distances) / len(distances), sum(norm_distances) / len(norm_distances)

def entropy(D):
	D = np.array(list(D), dtype=float)
	D /= D.sum()
	return -sum([p * np.log2(p) for p in D if p > 0])

def compute(band1, band2):
	table = []
	for lemma in lemma_map:
		if lemma_map[lemma][band1] and lemma_map[lemma][band2]:
			d1, nd1 = lexeme_distance(lemma_map[lemma][band1], words_by_band[band1])
			d2, nd2 = lexeme_distance(lemma_map[lemma][band2], words_by_band[band2])
			sparsity_increase = d2 - d1
			norm_sparsity_increase = nd2 - nd1
			h1 = entropy(lemma_map[lemma][band1].values())
			h2 = entropy(lemma_map[lemma][band2].values())
			entropy_increase = h2 - h1
			row = lemma, sparsity_increase, norm_sparsity_increase, entropy_increase
			table.append(row)
			print(row)
	df = pd.DataFrame(table)
	df.to_csv(ROOT / 'data' / 'sparsity_numbers1.csv')

def plot_regression_line(axis, x, y):
	lr = linregress(x, y)
	x = np.linspace(*axis.get_xlim(), 10)
	y = lr.slope * x + lr.intercept
	axis.plot(x, y, color='k')

def plot(df, axis, var, b1_label='b1', b2_label='b2'):
	axis.scatter(df[var], df['entropy_increase'], s=4, alpha=0.5, linewidths=0)
	plot_regression_line(axis, df['sparsity_increase'], df['entropy_increase'])
	axis.set_ylabel(f'Entropy increase from {b1_label} to {b2_label}')
	axis.set_xlabel(f'Sparsity increase from {b1_label} to {b2_label}')
	axis.set_title(f'Change from {b1_label} to {b2_label}')


corpus = json_read(ROOT / 'data' / 'helsinki_corpus.json')
lemma_map = json_read(ROOT / 'data' / 'lemma_map.json')

words_by_band = {
	'Old English': defaultdict(int),
	'Middle English': defaultdict(int),
	'Early Modern English': defaultdict(int)
}
for band, samples in corpus.items():
	for sample in samples:
		normalized_sample = normalize_text(' '.join(sample['text']))
		for word_token in normalized_sample.split(' '):
			if WORD_REGEX.fullmatch(word_token):
				words_by_band[band][word_token] += 1

# compute('Old English', 'Middle English')
# compute('Middle English', 'Early Modern English')





df1 = pd.read_csv(ROOT / 'data' / 'sparsity_numbers1.csv')
df2 = pd.read_csv(ROOT / 'data' / 'sparsity_numbers2.csv')

fig, axes = plt.subplots(1, 2, figsize=(6, 3))
plot(df1, axes[0], 'sparsity_increase', 'OE', 'ME')
plot(df2, axes[1], 'sparsity_increase', 'ME', 'EME')
fig.tight_layout()
fig.savefig(ROOT / 'manuscript' / 'figs' / 'sparsity_lev.pdf')

fig, axes = plt.subplots(1, 2, figsize=(6, 3))
plot(df1, axes[0], 'norm_sparsity_increase', 'OE', 'ME')
plot(df2, axes[1], 'norm_sparsity_increase', 'ME', 'EME')
fig.tight_layout()
fig.savefig(ROOT / 'manuscript' / 'figs' / 'sparsity_norm.pdf')

