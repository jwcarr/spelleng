from collections import defaultdict
from pathlib import Path
import pandas as pd


ROOT = Path(__file__).parent.parent.resolve()


BROAD_BANDS = ['Old English', 'Middle English', 'Early Modern English']


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


def convert_to_dict(mapping):
	'''
	Convert AU's CSV to a dictionary structure, which maps a written form from
	the corpus onto it's mapped meaning in the OED.
	'''
	new_mapping = defaultdict(list)
	for i, row in mapping.iterrows():
		new_mapping[ row['word'] ].append(
			(row['meaning'], row['meaning.attr'])
		)
	print(len(new_mapping))
	return new_mapping


if __name__ == '__main__':

	au_mapping = pd.read_csv(ROOT / 'data' / 'au_mapping.csv', na_filter=False)

	au_mapping = au_mapping[ au_mapping['meaning.attr'].isin(('n.', 'n.1', 'v.', 'v.1', 'adj.', 'adj.1')) ]

	print(au_mapping)

	au_mapping = convert_to_dict(au_mapping)

	print(au_mapping)


	# corpus = json_read(ROOT / 'data' / 'helsinki_corpus.json')
	# lemma_map = create_lemma_map(corpus, mapping, BROAD_BANDS)
	# json_write(lemma_map, ROOT / 'data' / 'lemma_map.json')


