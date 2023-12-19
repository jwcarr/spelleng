from collections import defaultdict
from pathlib import Path
import re
import numpy as np
from utils import json_read, json_write


ROOT = Path(__file__).parent.parent.resolve()


def zipfian_distribution(N, s=1):
	denom = sum([1 / n**s for n in range(1, N+1)])
	return np.array([(1 / k**s) / denom for k in range(1, N+1)])

def distribute_word_freq_across_lemmata(word_freqs, word_to_lemmata):
	lemmata_freqs = {}
	for word, lemmata in word_to_lemmata.items():
		# lemmata = [lemma for lemma in lemmata if lemma.split('_')[1] in ['n', 'n1' ]]
		lemmata = lemmata[0:1]
		freq = word_freqs[word]
		zipf_dist = zipfian_distribution(len(lemmata))
		freq_dist = zipf_dist * freq
		for lemma, freq in zip(lemmata, freq_dist):
			if lemma in lemmata_freqs:
				lemmata_freqs[lemma] += freq
			else:
				lemmata_freqs[lemma] = freq
	return {lemma: lemmata_freqs[lemma] for lemma in sorted(lemmata_freqs, key=lambda l: lemmata_freqs[l], reverse=True)}


if __name__ == '__main__':

	word_freqs = json_read(ROOT / 'data' / 'word_freqs.json')
	word_to_lemmata = json_read(ROOT / 'data' / 'words_to_lemmata.json')

	lemmata_freqs = distribute_word_freq_across_lemmata(word_freqs, word_to_lemmata)

	for lemma, freq in lemmata_freqs.items():
		print(lemma, freq)
