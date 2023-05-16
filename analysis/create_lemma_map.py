from collections import defaultdict
from pathlib import Path
import re
from utils import json_read, json_write


ROOT = Path(__file__).parent.parent.resolve()


def normalize_text(text):
	'''
	Convert a text to lowercase and strip all non-alphabetical characters.
	'''
	return re.sub(r'[^\w\s]', '', text.lower())


corpus = json_read(ROOT / 'data' / 'helsinki_corpus.json')
mapping = json_read(ROOT / 'data' / 'oed_mapping.json')

lemma_map = {}
for band, samples in corpus.items():
	for sample in samples:
		normalized_sample = normalize_text(' '.join(sample['text']))
		for form in normalized_sample.split(' '):
			if lemma := mapping.get(form, None):
				if lemma in lemma_map:
					lemma_map[lemma][band][form] += 1
				else:
					lemma_map[lemma] = {
						'Old English': defaultdict(int),
						'Middle English': defaultdict(int),
						'Early Modern English': defaultdict(int)
					}
					lemma_map[lemma][band][form] += 1

for lemma, data in lemma_map.items():
	for band, forms in data.items():
		lemma_map[lemma][band] = {
			form: forms[form]
			for form in sorted(forms, key=lambda w: forms[w], reverse=True)
		}

sorted_lemma_map = {}


def total_form_count(lemma):
	total_count = 0
	for band, forms in lemma_map[lemma].items():
		total_count += sum(forms.values())
	return total_count

lemma_map = {lemma: lemma_map[lemma] for lemma in sorted(lemma_map, key=lambda l: total_form_count(l), reverse=True)}

json_write(lemma_map, ROOT / 'data' / 'lemma_map.json')
