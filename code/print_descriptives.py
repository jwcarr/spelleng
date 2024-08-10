from pathlib import Path
import pandas as pd
import utils


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'


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
	spelleng = pd.read_csv(DATA / 'spelleng_quote.csv')
	n_lemmata = spelleng['lemma'].nunique()
	n_nouns = spelleng[ spelleng['pos'] == 'nn' ]['lemma'].nunique()
	n_adjectives = spelleng[ spelleng['pos'] == 'jj' ]['lemma'].nunique()
	n_verbs = spelleng[ spelleng['pos'] == 'vb' ]['lemma'].nunique()
	n_adverbs = spelleng[ spelleng['pos'] == 'rb' ]['lemma'].nunique()
	print(n_lemmata, n_nouns, n_adjectives, n_verbs, n_adverbs)


if __name__ == '__main__':
	
	print_corpus_counts()
	print_spelleng_counts()
