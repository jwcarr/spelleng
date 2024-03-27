from pathlib import Path
from collections import defaultdict
from utils import json_read, json_write


ROOT = Path(__file__).parent.parent.resolve()


def count_corpus(corpus):
	word_freqs = {band: defaultdict(int) for band in corpus}
	for band, documents in corpus.items():
		for document in documents:
			for token in document['text'].split(' '):
				word_freqs[band][token] += 1
		word_freqs[band] = {
			word: word_freqs[band][word]
			for word in sorted(word_freqs[band], key=lambda w: word_freqs[band][w], reverse=True)
		}
	return word_freqs


if __name__ == '__main__':

	corpus = json_read(ROOT / 'data' / 'corpus.json')

	word_freqs = count_corpus(corpus)

	json_write(word_freqs, ROOT / 'data' / 'word_freqs.json')
