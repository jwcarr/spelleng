import re
from collections import defaultdict
from pathlib import Path
from utils import json_read


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'


celex = json_read(DATA / 'celex_eml.json')


stem_extractor = re.compile(r'\((?P<stem>\w+?)\)\[(?P<pos>[NAV])\]')
stem_extractor = re.compile(r'.+?(ing|ed)')


def find_stems():
	stem_counts = defaultdict(int)
	for item_id, data in celex.items():
		if stem_match := stem_extractor.search(data['StrucLab']):

			stem_counts[ stem_match.group(0) ] += 1
	return stem_counts


def get_stem_family(stem):
	family = {}
	for word, segmentation in morpholex.items():
		if stem in segmentation['roots']:
			family[word] = ''
	return family


print(find_stems())