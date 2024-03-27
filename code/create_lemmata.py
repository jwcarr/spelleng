from collections import defaultdict
from pathlib import Path
import re
import numpy as np
from utils import json_read


ROOT = Path(__file__).parent.parent.resolve()
LEMMA_RE = re.compile(r'^[a-z]{4,}$')


def zipfian_distribution(N, s=2):
	denom = sum([1 / n**s for n in range(1, N+1)])
	return np.array([(1 / k**s) / denom for k in range(1, N+1)])

def distribute_word_freq_across_lemmata(word_freqs, word_to_lemmata):
	lemmata_freqs = {}
	for word, lemmata in word_to_lemmata.items():
		freq = word_freqs[word]
		zipf_dist = zipfian_distribution(len(lemmata))
		freq_dist = zipf_dist * freq
		for lemma, freq in zip(lemmata, freq_dist):
			if lemma in lemmata_freqs:
				lemmata_freqs[lemma] += freq
			else:
				lemmata_freqs[lemma] = freq
	return {lemma: lemmata_freqs[lemma] for lemma in sorted(lemmata_freqs, key=lambda l: lemmata_freqs[l], reverse=True) if lemmata_freqs[lemma] >= 1}

def load_stop_words():
	with open(ROOT / 'data' / 'nltk_stop_words.txt') as file:
		stop_words = file.read().split('\n')
	return stop_words

def filter_lemmata(dict, POS):
	if isinstance(POS, str):
		POS = [POS]
	stop_words = load_stop_words()
	filtered_dict = {}
	for k, v in dict.items():
		lemma, pos = k.split('_')
		if pos in POS and lemma not in stop_words and LEMMA_RE.fullmatch(lemma):
			filtered_dict[k] = v
	return filtered_dict

def remove_duplicates(original_lemmata):
	form_to_lemmata = defaultdict(list)
	for lemma, freq in original_lemmata.items():
		form_to_lemmata[ lemma.split('_')[0] ].append(lemma)
	deduplicated_lemmata = {}
	for form, lemmata in form_to_lemmata.items():
		lemma = max(lemmata)
		deduplicated_lemmata[lemma] = original_lemmata[lemma]
	return deduplicated_lemmata


if __name__ == '__main__':

	parts_of_speech = [['n', 'n1'], ['v', 'v1'], ['adj', 'adj1']]

	for POS in parts_of_speech:

		word_freqs = json_read(ROOT / 'data' / 'word_freqs.json')
		words_to_lemmata = json_read(ROOT / 'data' / 'words_to_lemmata.json')

		lemmata_freqs = distribute_word_freq_across_lemmata(word_freqs, words_to_lemmata)
		
		lemmata_freqs = filter_lemmata(lemmata_freqs, POS)

		lemmata_freqs = remove_duplicates(lemmata_freqs)

		output = '\n'.join(lemmata_freqs.keys())

		with open(ROOT / 'data' / f'lemmata_{POS[0]}.txt', 'w') as file:
			file.write(output)
