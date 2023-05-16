from pathlib import Path
from collections import defaultdict
import re
import pandas
from utils import json_write


ROOT = Path(__file__).parent.parent.resolve()

WORD_REGEX = re.compile(r'[abcdefghijklmnopqrstuvwxyzæðþęłȝꝥ]+')


def convert_to_dict(input_csv):
	'''
	Convert AU's CSV to a dictionary structure, which maps a written form from
	the corpus onto it's mapped meaning in the OED.
	'''
	mapping = pandas.read_csv(input_csv, na_filter=False)
	new_mapping = defaultdict(list)
	for i, row in mapping.iterrows():
		new_mapping[ row['word'] ].append(
			(row['meaning'], row['meaning.attr'])
		)
	print(len(new_mapping))
	return new_mapping
	
def reduce_mapping_to_unique_lemma(mapping):
	'''
	Remove words that were mapped to multiple possible meanings. E.g. ðing is
	mapped to thing, something, and think.
	'''
	new_mapping = {}
	for word, mapped_meanings in mapping.items():
		unique_headwords = set([headword for headword, attributes in mapped_meanings])
		if len(unique_headwords) == 1:
			new_mapping[word] = list(unique_headwords)[0]
	print(len(new_mapping))
	return new_mapping

def filter_words_with_nonalpha_chars(mapping):
	new_mapping = {}
	for word, meaning in mapping.items():
		if word_match := WORD_REGEX.fullmatch(word):
			new_mapping[word] = meaning
	print(len(new_mapping))
	return new_mapping


if __name__ == '__main__':

	mapping = convert_to_dict(ROOT / 'data' / 'au_mapping.csv')
	mapping = reduce_mapping_to_unique_lemma(mapping)
	mapping = filter_words_with_nonalpha_chars(mapping)
	json_write(mapping, ROOT / 'data' / 'oed_mapping.json')
