from pathlib import Path
import re
import pandas as pd
import utils
import oed_extract
import warnings


warnings.filterwarnings("ignore")


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'
SPELLENG = ROOT / 'spelleng'


spelleng = pd.read_csv(SPELLENG / 'spelleng_quote.csv')
spelleng = spelleng.dropna(how='any')


def find_words(target_spelling, target_pronuncation):
	if isinstance(target_spelling, list):
		target_spelling = '(' + '|'.join(target_spelling) + ')'
	lemmata_ending_with_sound    = set(spelleng[spelleng['pronunciation'].str.contains(target_pronuncation)]['lemma_id'].unique())
	lemmata_ending_with_spelling = set(spelleng[spelleng['headword'].str.contains(target_spelling)]['lemma_id'].unique())
	return sorted(list(lemmata_ending_with_sound - lemmata_ending_with_spelling))


search_queries = [
	('-Y', 'y$', r'i$'),
	('-AL', 'al$', r'əl$'),
	('-OUS', '(ness|less|ous)$', r'[^ɪ]əs$'),
	('-IC', 'ic$', r'[^ʌe]ɪk$'),

	('UN-', '^un', r'^ʌn'),
	('DIS-', '^dis', r'^dɪs'),
	('MIS-', '^mis', r'^m(ɪ|ᵻ)s'),

	('-NESS', 'ness$', r'nəs$'),
	('-LESS', 'less$', r'ləs$'),
	('-FUL', 'ful$', r'f\(?(ᵿ|ʊ)\)?l$'),
	('-ABLE', 'able$', r'əb\(?ə?\)?l$'),
	('-MENT', 'ment$', r'mənt$'),
	('-ITY', 'ity$', r'(ᵻ|ɪ|ə)ti$'),
	('-SHIP', 'ship$', r'[^t]ʃɪp$'),
	('-ATION', 'ation$', r'eɪʃə?n$'),
]



for affix, spelling, pronunciation in search_queries:
	candidates = find_words(spelling, pronunciation)
	print(affix)
	print(f'Lemmata pronounced /{pronunciation}/ but not spelled <{spelling}>:')
	print(', '.join(candidates))
	print()




quit()

# lemmata = list(spelleng['lemma_id'].unique())

# affixes = utils.json_read(DATA / 'oed_affixes.json')

# affix_derivatives = {}

# for affix in affixes:
# 	print(affix)
# 	affix_form, affix_type = affix.split('_')
# 	if affix_type.startswith('prefix'):
# 		valid_re = re.compile(f'^{affix_form}')
# 	else:
# 		valid_re = re.compile(f'{affix_form}_')
# 	lp = oed_extract.OEDLemmaParser(affix)
# 	lp.access()
# 	affix_derivatives[affix] = sorted([
# 		derivative
# 		for derivative in lp.get_derivatives() if derivative in lemmata and valid_re.search(derivative)
# 	])

# utils.json_write(affix_derivatives, DATA / 'affix_derivatives.json')




# affix_derivatives = utils.json_read(DATA / 'affix_derivatives.json')

# for affix, derivatives in affix_derivatives.items():
# 	print(str(len(derivatives)).zfill(3), affix)
	
