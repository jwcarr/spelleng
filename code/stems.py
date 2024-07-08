from collections import defaultdict
from pathlib import Path
import re
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt

plt.rcParams.update({'font.sans-serif': 'Helvetica Neue', 'font.size': 7})


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'
SPELLENG = ROOT / 'spelleng'


spelleng = pd.read_csv(SPELLENG / 'spelleng_quote.csv', keep_default_na=False)


parsers = {
	'ness': re.compile(r'^(?P<stem>\w+)(?P<suff>nesse|ness|niss|nes|nis)$'),
	'ion':  re.compile(r'^(?P<stem>\w+)(?P<suff>ion)$'),
	'ism':  re.compile(r'^(?P<stem>\w+)(?P<suff>ism)$'),
	'ly':  re.compile(r'^(?P<stem>\w+)(?P<suff>ley|lee|ly|li|le)$'),
	'tion':  re.compile(r'^(?P<stem>\w+)(?P<suff>ssion|sion|tion|cion|cyon)$'),
}

suffix_parser = re.compile(r'^(?P<stem>\w+)(?P<suff>' + '|'.join([suff for suff in parsers]) + ')$')




def analyse_lemma(counts):
	headword = list(counts['headword'].unique())[0]
	stems = defaultdict(list)
	if parsed_headword := suffix_parser.match(headword):
		historical_parser = parsers[ parsed_headword['suff'] ]
		for variant, variant_counts in counts.groupby('variant'):
			if parsed_variant := historical_parser.match(variant):
				stems[ parsed_variant['stem'] ].append(variant_counts)
	for stem, stem_counts in stems.items():
		stem_counts = pd.concat(stem_counts, ignore_index=True)
		print(stem)
		print(stem_counts)



def analyse_stem_set(counts):
	for lemma_id, lemma_counts in counts.groupby('lemma_id'):
		analyse_lemma(lemma_counts)



absolut = spelleng[ spelleng['headword'].str.contains('^absolut') ]
print(absolut)
analyse_stem_set(absolut)


# tion_parser = re.compile(r'^(?P<stem>\w+?)(?P<cons>ss|tt|cc|sh|s|t|c|x)(?P<suff>ioun|ione|yone|ion|yon|on)$')

# def get_variant_stems(counts):
# 	variants = list(counts['variant'])
# 	for variant in variants:
# 		if variant_match := tion_parser.match(variant):
# 			print(variant_match['cons'])


# tion = spelleng[ spelleng['headword'].str.contains(r'\w+(ssion|sion|tion|cion)$') ]
# for lemma_id, subset in tion.groupby('lemma_id'):
# 	get_variant_stems(subset)
















