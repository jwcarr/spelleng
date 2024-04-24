from pathlib import Path
from utils import json_read, json_write


ROOT = Path(__file__).parent.parent.resolve()


def extract_lemmata(corpus, taget_POS_rewrites, at_least_n_length, at_least_n_documents):
	word_freqs = {}
	for band, documents in corpus.items():
		if band.startswith('Late Modern English'):
			for document_i, document in enumerate(documents):
				document_id = f'{band} {document_i}'
				for token in document['text'].split(' '):
					word, pos = token.split('_')
					if len(word) < at_least_n_length:
						continue
					if pos in taget_POS_rewrites:
						word_pos = f'{word}_{taget_POS_rewrites[pos]}'
						if word_pos in word_freqs:
							word_freqs[word_pos][0] += 1
							word_freqs[word_pos][1].add(document_id)
						else:
							word_freqs[word_pos] = [1, {document_id}]
	word_freqs = {
		word: freq
		for word, (freq, documents) in word_freqs.items() if len(documents) >= at_least_n_documents
	}
	word_freqs = {
		word: word_freqs[word]
		for word in sorted(word_freqs, key=lambda w: word_freqs[w], reverse=True)
	}
	return word_freqs


if __name__ == '__main__':

	corpus = json_read(ROOT / 'data' / 'corpus.json')

	lemmata = extract_lemmata(
		corpus,
		taget_POS_rewrites={'nn': 'n', 'vb': 'v', 'jj': 'adj'},
		at_least_n_length=3,
		at_least_n_documents=3,
	)

	# remove modals
	del(lemmata['have_v'])
	del(lemmata['can_v'])
	del(lemmata['will_v'])

	json_write(lemmata, ROOT / 'data' / 'lemmata.json')

	print('# lemmata:', len(lemmata))
	for pos in ['n', 'adj', 'v']:
		print(f'# {pos}:', len([token for token in lemmata if token.endswith(f'_{pos}')]))
