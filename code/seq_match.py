from difflib import SequenceMatcher

def junk(element):
	return element in '<>'

seq_matcher = SequenceMatcher(isjunk=junk)

def replace_vowels(form):
	new_form = ''
	for letter in form:
		if letter in 'aeiou':
			new_form += 'V'
		else:
			new_form += letter
	return new_form

categories = {
	'a': 'Vb',
	'b': 'C',
	'c': 'C',
	'd': 'C',
	'e': 'Vs',
	'f': 'C',
	'g': 'C',
	'h': 'C',
	'i': 'Vs',
	'j': 'C',
	'k': 'C',
	'l': 'C',
	'm': 'C',
	'n': 'C',
	'o': 'Vb',
	'p': 'C',
	'q': 'C',
	'r': 'C',
	's': 'C',
	't': 'C',
	'u': 'Vb',
	'v': 'C',
	'w': 'C',
	'x': 'C',
	'y': 'Vs',
	'z': 'C',
}


def insert(insertion, prev, foll):
	if insertion == 'e' and foll == '':
		return '$', 'e$'
	if prev == '':
		return foll, insertion + foll
	if foll == '':
		return prev, prev + insertion
	if insertion == prev:
		return prev, prev + insertion
	if insertion == foll:
		return foll, insertion + foll
	if categories[insertion] == categories[prev]:
		return prev, prev + insertion
	if categories[insertion] == categories[foll]:
		return foll, insertion + foll
	return prev, prev + insertion

def delete(deletion, prev, foll):
	if prev == '':
		return deletion + foll, foll
	if foll == '':
		return prev + deletion, prev
	if deletion == prev:
		return prev + deletion, prev
	if deletion == foll:
		return deletion + foll, foll
	if categories[deletion] == categories[prev]:
		return prev + deletion, prev
	if categories[deletion] == categories[foll]:
		return deletion + foll, foll
	return prev, prev + deletion


	

def compare(form1, form2):
	transformations = []
	if form1 == form2:
		return transformations
	seq_matcher.set_seqs(form1, form2)
	for code, f1s, f1e, f2s, f2e in seq_matcher.get_opcodes():
		if code == 'replace':
			part1 = form1[f1s:f1e]
			part2 = form2[f2s:f2e]
			transformations.append(f'{part1}→{part2}')
		elif code == 'delete':
			deletion = form1[f1s:f1e]
			part1, part2 = delete(deletion, form2[f2s-1:f2s], form2[f2s:f2s+1])
			transformations.append(f'{part1}→{part2}')
		elif code == 'insert':
			insertion = form2[f2s:f2e]
			part1, part2 = insert(insertion, form1[f1s-1:f1s], form1[f1s:f1s+1])
			transformations.append(f'{part1}→{part2}')
	return transformations



assert compare('publique', 'publick')[0] == 'que→ck'
assert compare('delicius', 'delicious')[0] == 'u→ou'
assert compare('delicious', 'deliciouss')[0] == 's→ss'
assert compare('delicious', 'deliciouse')[0] == '$→e$'



