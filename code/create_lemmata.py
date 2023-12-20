from pathlib import Path
import numpy as np
from utils import json_read


ROOT = Path(__file__).parent.parent.resolve()


def zipfian_distribution(N, s=1):
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
	return {lemma: lemmata_freqs[lemma] for lemma in sorted(lemmata_freqs, key=lambda l: lemmata_freqs[l], reverse=True)}

def filter_part_of_speech(dict, pos):
	if isinstance(pos, str):
		pos = [pos]
	return {k: v for k, v in dict.items() if k.split('_')[1] in pos}


if __name__ == '__main__':

	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('pos', action='store', type=str, help='parts of speech (comma separated)')
	args = parser.parse_args()

	parts_of_speech = args.pos.split(',')

	word_freqs = json_read(ROOT / 'data' / 'word_freqs.json')
	words_to_lemmata = json_read(ROOT / 'data' / 'words_to_lemmata.json')

	lemmata_freqs = distribute_word_freq_across_lemmata(word_freqs, words_to_lemmata)
	lemmata_freqs_filtered = filter_part_of_speech(lemmata_freqs, parts_of_speech)

	for i, lemma in enumerate(lemmata_freqs_filtered):

		if input(f'{i} {lemma}: ') == '':

			with open(ROOT / 'data' / f'lemmata_{parts_of_speech[0]}.txt', 'a') as file:
				file.write(lemma + '\n')
