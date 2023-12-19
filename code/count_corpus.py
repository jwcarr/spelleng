from collections import defaultdict
from pathlib import Path
import re
from utils import json_read, json_write


ROOT = Path(__file__).parent.parent.resolve()

WORD_REGEX = re.compile(r'[abcdefghijklmnopqrstuvwxyzæðþęłȝꝥ]+')


def normalize_text(text):
	'''
	Convert a text to lowercase and strip all non-alphabetical characters.
	'''
	return re.sub(r'[^\w\s]', '', text.lower())

def count_corpus(corpus):
	word_freqs = defaultdict(int)
	for band, samples in corpus.items():
		for sample in samples:
			for line in sample['text']:
				for word in normalize_text(line).split(' '):
					if WORD_REGEX.fullmatch(word):
						word_freqs[word] += 1
	return word_freqs


if __name__ == '__main__':

	corpus = json_read(ROOT / 'data' / 'helsinki_corpus_broad.json')

	words = count_corpus(corpus)

	json_write(words, ROOT / 'data' / 'word_freqs.json')
