from collections import defaultdict
import re
from pathlib import Path
from utils import json_read
import Levenshtein

ROOT = Path(__file__).parent.parent.resolve()

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


corpus = json_read(ROOT / 'data' / 'helsinki_corpus.json')

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


for band, words in words_by_band.items():

	word_counts = reduce(words, n=3000)
	values_to_probs(word_counts, weighted=False)
	print(calculate_density(word_counts))
