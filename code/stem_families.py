import re
from collections import defaultdict
from pathlib import Path
import utils


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'


celex_eml = utils.json_read(DATA / 'celex_eml.json')
celex_emw = utils.json_read(DATA / 'celex_emw.json')


stem_extractor = re.compile(r'\((?P<stem>[a-z]+?)\)\[(?P<pos>[NAV])\]')
re_valid_word = re.compile(r'[a-z]+')

CELEX_POS_MAP = {'N': 'nn', 'V': 'vb', 'A': 'jj', 'ADV': 'rb'}


def find_stems():
	stem_counts = defaultdict(list)
	for lemma_id, data in celex_eml.items():
		lemma_form = data['Head']
		lemma_pos = data['pos']
		if not re_valid_word.fullmatch(lemma_form) or lemma_pos not in ('N', 'A', 'V', 'ADV'):
			continue
		lemma = f'{lemma_form}_{CELEX_POS_MAP[lemma_pos]}'
		for stem_form, stem_pos in stem_extractor.findall(data['StrucLab']):
			candidate_stems = celex_emw[stem_form]
			candidate_stems = [stem['IdNumLemma'] for stem in candidate_stems if stem['pos'] == stem_pos]
			stem_celex_id = list(set(candidate_stems))[0]
			stem_form = celex_eml[stem_celex_id]['Head']
			stem_pos = CELEX_POS_MAP[ celex_eml[stem_celex_id]['pos'] ]
			stem = f'{stem_form}_{stem_pos}'
			stem_counts[ stem ].append(lemma)
	return stem_counts


if __name__ == '__main__':

	stem_map = find_stems()
	stem_map = {k: stem_map[k] for k in sorted(list(stem_map.keys()))}
	utils.json_write(stem_map, DATA / 'stem_map.json')
