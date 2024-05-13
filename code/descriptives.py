from pathlib import Path
import pandas as pd
import utils


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'
SPELLENG = ROOT / 'spelleng'


def print_corpus_counts():
	corpus = utils.json_read(DATA / 'corpus.json')
	corpus_count = utils.json_read(DATA / 'corpus_count.json')

	total_texts = 0
	total_tokens = 0
	all_types = set()

	for band, tokens in corpus_count.items():
		n_texts = len(corpus[band])
		total_texts += n_texts
		n_tokens = sum(tokens[t][1] for t in tokens)
		total_tokens += n_tokens
		types = set([token.split('_')[0] for token in tokens])
		n_types = len(types)
		all_types.update(types)
		print(band, n_texts, n_tokens, n_types)

	print(total_texts, total_tokens, len(all_types))


def print_spelleng_counts():
	spelleng = pd.read_csv(SPELLENG / 'spelleng_quote2.csv')
	n_lemmata = spelleng['lemma_id'].nunique()
	n_nouns = spelleng[ spelleng['part_of_speech'] == 'n' ]['lemma_id'].nunique()
	n_adjectives = spelleng[ spelleng['part_of_speech'] == 'a' ]['lemma_id'].nunique()
	n_verbs = spelleng[ spelleng['part_of_speech'] == 'v' ]['lemma_id'].nunique()
	print(n_lemmata, n_nouns, n_adjectives, n_verbs)


if __name__ == '__main__':
	
	# print_corpus_counts()
	print_spelleng_counts()
