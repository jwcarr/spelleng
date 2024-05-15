from pathlib import Path
import re
import pandas as pd
import utils


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'
SPELLENG = ROOT / 'spelleng'


oed_affixes = utils.json_read(DATA / 'oed_affixes.json')
historical_form_parsers = {
	'ness': re.compile(r'^(?P<stem>\w+)(?P<suff>nesse|ness|nis)$'),
	'tion': re.compile(r'^(?P<stem>\w+[tsc])(?P<suff>ion|ioun|iun|oun|yon|ion)$'),
	'ism':  re.compile(r'^(?P<stem>\w+)(?P<suff>ism)$'),
	'ly':   re.compile(r'^(?P<stem>\w+)(?P<suff>ly)$'),
}

suffix_parser = re.compile(r'^(?P<stem>\w+)(?P<suff>ness|tion|ism|ly)$')

# histrorical_ity_stemmer = re.compile(r'^(?P<stem>\w+)(?P<suffix>atie|itie|itee|ytye|ety|yty|ite|iti|ity)$')


spelleng = pd.read_csv(SPELLENG / 'spelleng_quote.csv', keep_default_na=False)


# ity_lemmata = spelleng[ spelleng['headword'].str.contains(r'ity$') ]


def analyze_stem_family(stem, df):
	print('STEM', stem)
	for lemma_id, subset in df.groupby('lemma_id'):
		headword = subset['headword'].unique()[0]
		# print('HEAD', headword)
		variants = list(subset['variant'])
		if suffix_match := suffix_parser.match(headword):
			suffix = suffix_match['suff']
			form_parser = historical_form_parsers[suffix]
			for variant in variants:
				if form_match := form_parser.match(variant):
					print(variant, form_match['stem'])
	print()
			



for stem, subset in spelleng.groupby('stem'):
	# if stem == 'absolut':
	if len(subset['lemma_id'].unique()) > 1:
		analyze_stem_family(stem, subset)
