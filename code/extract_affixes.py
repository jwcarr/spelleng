from pathlib import Path
import re
import pandas as pd
import utils
import oed_extract


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'
SPELLENG = ROOT / 'spelleng'


spelleng = pd.read_csv(SPELLENG / 'spelleng_quote.csv')
spelleng = spelleng.dropna(how='any')

def find_words(target_spelling, target_pronuncation):
	if isinstance(target_spelling, list):
		target_spelling = '(' + '|'.join(target_spelling) + ')'
	lemmata_ending_with_sound    = set(spelleng[spelleng['pronunciation'].str.contains(f'{target_pronuncation}$')]['lemma_id'].unique())
	lemmata_ending_with_spelling = set(spelleng[spelleng['headword'].str.contains(f'{target_spelling}$')]['lemma_id'].unique())
	print(f'Words that end /{target_pronuncation}/ but are not spelled <{target_spelling}>:')
	print(sorted(list(lemmata_ending_with_sound - lemmata_ending_with_spelling)))
	# print(f'Words that end <{target_spelling}> but are not pronounced /{target_pronuncation}/:')
	# print(sorted(list(lemmata_ending_with_spelling - lemmata_ending_with_sound)))

# find_words('ation', 'eɪʃə?n')
# find_words('ship', 'ʃɪp')
# find_words('ness', 'n(ᵻ|ɪ|ə)s')
# find_words('y', 'i')
# find_words(['ness', 'less', 'ous'], 'əs')
# find_words('less', 'l(ᵻ|ɪ|ə)s')
# find_words('ful', r'f\(?(ᵿ|ʊ)\)?l')
find_words('able', 'əb\(?ə?\)?l')





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




affix_derivatives = utils.json_read(DATA / 'affix_derivatives.json')

for affix, derivatives in affix_derivatives.items():
	print(str(len(derivatives)).zfill(3), affix)
	
