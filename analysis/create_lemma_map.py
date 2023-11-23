from collections import defaultdict
from pathlib import Path
import re
from utils import json_read, json_write


ROOT = Path(__file__).parent.parent.resolve()

BROAD_BANDS = ['Old English', 'Middle English', 'Early Modern English']
NARROW_BANDS = [
	'Old English (I)', 'Old English (II)', 'Old English (III)', 'Old English (IV)',
	'Middle English (I)', 'Middle English (II)', 'Middle English (III)', 'Middle English (IV)',
	'Early Modern English (I)', 'Early Modern English (II)', 'Early Modern English (III)'
]


def normalize_text(text):
	'''
	Convert a text to lowercase and strip all non-alphabetical characters.
	'''
	return re.sub(r'[^\w\s]', '', text.lower())

def create_lemma_map(corpus, mapping, banding):
	lemma_map = {}
	for band, samples in corpus.items():
		for sample in samples:
			normalized_sample = normalize_text(' '.join(sample['text']))
			for form in normalized_sample.split(' '):
				if lemma := mapping.get(form, None):
					if lemma in lemma_map:
						lemma_map[lemma][band][form] += 1
					else:
						lemma_map[lemma] = {b: defaultdict(int) for b in banding}
						lemma_map[lemma][band][form] += 1
	for lemma, data in lemma_map.items():
		for band, forms in data.items():
			lemma_map[lemma][band] = {
				form: forms[form]
				for form in sorted(forms, key=lambda w: forms[w], reverse=True)
			}

	def total_form_count(lemma):
		total_count = 0
		for band, forms in lemma_map[lemma].items():
			total_count += sum(forms.values())
		return total_count

	return {lemma: lemma_map[lemma] for lemma in sorted(lemma_map, key=total_form_count, reverse=True)}


if __name__ == '__main__':

	mapping = json_read(ROOT / 'data' / 'oed_mapping.json')

	corpus = json_read(ROOT / 'data' / 'helsinki_corpus.json')
	lemma_map = create_lemma_map(corpus, mapping, BROAD_BANDS)
	json_write(lemma_map, ROOT / 'data' / 'lemma_map.json')

	corpus = json_read(ROOT / 'data' / 'helsinki_corpus_subbanded.json')
	lemma_map = create_lemma_map(corpus, mapping, NARROW_BANDS)
	json_write(lemma_map, ROOT / 'data' / 'lemma_map_subbanded.json')
