from collections import defaultdict
from pathlib import Path
from utils import json_read, json_write
import numpy as np
import matplotlib.pyplot as plt


ROOT = Path(__file__).parent.parent.resolve()

BANDS = ['Old English', 'Middle English', 'Early Modern English']

oed_attested_forms = {
	'ness': ['nace', 'nas', 'nase', 'nasse', 'nece', 'nes', 'nesce', 'nesch', 'nese', 'ness', 'nessche', 'nesse', 'nesshe', 'nez', 'nis', 'nise', 'niss', 'nisse', 'nus', 'nuss', 'nys', 'nyss', 'nysse', 'næs'],
	'ful':  ['fa', 'ffol', 'fful', 'ffull', 'fil', 'fol', 'fole', 'folle', 'foo', 'fou', 'foul', 'foull', 'fow', 'fu', 'ful', 'fule', 'full', 'fulle', 'fwll', 'uel', 'uol', 'uull', 'vul'],
	'ous':  ['es', 'is', 'ois', 'os', 'ose', 'ous', 'ouse', 'ows', 'owse', 'us', 'ys'],
	'ic':   ['ic', 'ick', 'ik', 'ike', 'ique', 'icke', 'ycke', 'eck', 'yk', 'yke'],
	'al':   ['ale', 'alle', 'ell', 'el', 'al', 'all'],
	'ship': ['chep', 'chepe', 'chipe', 'chyp', 'scep', 'schepe', 'schip', 'schipe', 'schippe', 'schupe', 'schuppe', 'schyp', 'sciop', 'scip', 'scipe', 'scype', 'shep', 'ship', 'shipe', 'shipp', 'shippe', 'shyp', 'shyppe', 'sip', 'skiepe'],
	'less': ['las', 'lase', 'leas', 'lease', 'lees', 'les', 'lese', 'less', 'lesse', 'lez', 'leæs', 'lias', 'lies', 'liese', 'lis', 'lyas', 'læs'],
}

lemma_map = json_read(ROOT / 'data' / 'lemma_map.json')

suffix_colors = {
	'alle': 'blue',
	'ale': 'orange',
	'ell': 'green',
	'all': 'red',
	'el': 'purple',
	'al': 'pink',
}

def plot_spelling_stack(stack, forms, title=None):
	reduced_stack = []
	reduced_forms = []
	for row, form in zip(stack, forms):
		if row.sum() > 0:
			reduced_stack.append(row)
			reduced_forms.append(form)
	reduced_stack = np.array(reduced_stack)
	for j in range(len(BANDS)):
		reduced_stack[:, j] /= reduced_stack[:, j].sum()
	fig, axis = plt.subplots(1, 1)
	axis.stackplot([0, 1, 2], reduced_stack, labels=reduced_forms, colors=[suffix_colors[form] for form in reduced_forms])
	axis.legend(fontsize=8)
	axis.set_ylim(0, 1)
	axis.set_ylabel('Proportion of attested spellings')
	axis.set_xticks([0, 1, 2])
	axis.set_xticklabels(BANDS)
	axis.set_xlim(0, 2)
	axis.set_title(title)
	plt.show()

def which_suffix(word, suffix_forms):
	for i, suffix_form in enumerate(suffix_forms):
		if word.endswith(suffix_form):
			return i
	return None

celex_status_codes = {
	'M': 'Monomorphemic',
	'Z': 'Zero derivation',
	'F': 'Contracted form',

	'C': 'Complex',

	'W': 'Complex (but different suffix)',

	'I': 'Morphological analysis unavailable in Celex',
	'O': 'Morphological analysis unavailable in Celex',
	'R': 'Morphological analysis unavailable in Celex',
	'U': 'Morphological analysis unavailable in Celex',

	'X': 'Word not in Celex',
}

def parse_morph(suffix):
	lemmas_by_status_code = defaultdict(list)
	for lemma, data in lemma_map.items():
		lemma = lemma.lower()
		if lemma.endswith(suffix):
			if lemma in eml:
				if eml[lemma][0] == 'C':
					if f'({suffix})' in eml[lemma][1]:
						code = eml[lemma][0]
					else:
						code = 'W'
				else:
					code = eml[lemma][0]
			else:
				code = 'X'

			if code in ['I', 'O', 'R']:
				code = 'U'
			lemmas_by_status_code[code].append(lemma)

	print(f'-{suffix.upper()}')
	# print()
	# for code, description in celex_status_codes.items():
	# 	if lemmas_by_status_code[code]:
	# 		print(description)
	# 		print(', '.join(sorted(lemmas_by_status_code[code])))
	# 		print()
	
	print(len(lemmas_by_status_code['C']), len(lemmas_by_status_code['M']) + len(lemmas_by_status_code['Z']))






def count_spellings_of_suffix(suffix, include_only=None):
	suffixed_lemmas = {}
	for lemma, data in lemma_map.items():
		lemma = lemma.lower()
		if isinstance(include_only, list):
			if lemma not in include_only:
				continue
		if lemma.endswith(suffix):
			suffixed_lemmas[lemma] = data
	suffix_forms = sorted(oed_attested_forms[suffix], key=lambda f: -len(f))
	counts = np.zeros((len(suffix_forms), len(BANDS)), dtype=float)
	for lemma, data in suffixed_lemmas.items():
		print(lemma.upper())
		print()
		for band, word_forms in data.items():
			print('    ' + band)
			print('        ' + ', '.join(sorted(list(word_forms))))
			print()
			j = BANDS.index(band)
			for word_form, count in word_forms.items():
				if (i := which_suffix(word_form, suffix_forms)) is None:
					pass
					# print(f'Cannot map "{word_form}" to -{suffix} suffix')
				else:
					counts[i, j] += count
	return counts, suffix_forms

def parse_celex_emw(data_path):
	celex = {}
	with open(data_path, encoding='ascii') as file:
		for line in file:
			data = line.strip().split('\\')
			word = data[1].lower()
			status = data[3]
			desc = data[21]
			if word not in celex:
				celex[word] = (status, desc)
	return celex


al_mono = ['admiral', 'animal', 'anneal', 'canal', 'cathedral', 'coal', 'conceal', 'corporal', 'crystal', 'funeral', 'gal', 'goal', 'heal', 'hospital', 'leal', 'marshal', 'meal', 'metal', 'ordeal', 'rascal', 'rival', 'scandal', 'seal', 'seneschal', 'shoal', 'steal', 'teal', 'vassal', 'veal', 'victual', 'weal', 'zeal', 'aerial', 'appeal', 'capital', 'cardinal', 'chemical', 'coral', 'cordial', 'deal', 'equal', 'essential', 'final', 'fundamental', 'general', 'liberal', 'local', 'manual', 'material', 'menial', 'moral', 'mortal', 'musical', 'natural', 'official', 'ordinal', 'original', 'oval', 'pastoral', 'potential', 'principal', 'real', 'repeal', 'special', 'spiritual', 'total', 'vertical', 'virginal']
al_comp = ['accidental', 'acquittal', 'additional', 'arrival', 'autumnal', 'bridal', 'burial', 'comical', 'conjectural', 'continual', 'critical', 'denial', 'disposal', 'espousal', 'fatal', 'instrumental', 'internal', 'latitudinal', 'longitudinal', 'mechanical', 'medicinal', 'memorial', 'missal', 'mystical', 'naval', 'occidental', 'oriental', 'parental', 'personal', 'physical', 'proposal', 'recital', 'refusal', 'rehearsal', 'removal', 'rental', 'sacramental', 'signal', 'supernatural', 'testimonial', 'tidal', 'trial', 'universal', 'unnatural', 'verbal']

counts, suffix_forms = count_spellings_of_suffix('al', include_only=al_comp)
plot_spelling_stack(counts, suffix_forms, title='Complex lexemes')

counts, suffix_forms = count_spellings_of_suffix('al', include_only=al_mono)
plot_spelling_stack(counts, suffix_forms, title='Monomorphemic lexemes')

quit()


eml = parse_celex_emw(ROOT / '..' / 'wp1' / 'data' / 'celex2' / 'english' / 'eml' / 'eml.cd')

for suffix in ['able', 'age', 'al', 'ance', 'ate', 'dom', 'ee', 'en', 'ence', 'er', 'ese', 'ful', 'hood', 'ian', 'ible', 'ic', 'ify', 'ise', 'ish', 'ism', 'ist', 'ity', 'ive', 'ize', 'less', 'ly', 'ment', 'ness', 'or', 'ous', 'ry', 'ship', 'sion', 'tion', 'ty', 'ward', 'wise']:
	parse_morph(suffix)


