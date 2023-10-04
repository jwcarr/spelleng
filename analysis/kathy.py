from pathlib import Path
from utils import json_read, json_write
import pandas as pd


ROOT = Path(__file__).parent.parent.resolve()

BANDS = ['Old English', 'Middle English', 'Early Modern English']


lemma_map = json_read(ROOT / 'data' / 'lemma_map.json')

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

def count(target):
	count_all_three = 0
	count_1_and_2 = 0
	count_2_and_3 = 0
	for lemma, data in lemma_map.items():
		n1 = len(data['Old English'])
		n2 = len(data['Middle English'])
		n3 = len(data['Early Modern English'])
		if n1 >= target and n2 >= target and n3 >= target:
			count_all_three += 1
		if n1 >= target and n2 >= target:
			count_1_and_2 += 1
		if n2 >= target and n3 >= target:
			count_2_and_3 += 1
	print(count_all_three, count_1_and_2, count_2_and_3)

def parse_morph(suffix):
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




def kathy_spreadsheet():
	table = []
	header = [
		'lexeme',
		'n spellings',
		'n spellings band 1',
		'n spellings band 2',
		'n spellings band 3',
		'n bands',
		'morph status',
	]
	for lemma, data in lemma_map.items():
		if lemma in eml:
			morph = eml[lemma][0]
		else:
			morph = 'X'
		table.append([
			lemma,
			len(set(list(data['Old English'].keys()) + list(data['Middle English'].keys()) + list(data['Early Modern English'].keys()))),
			len(data['Old English']),
			len(data['Middle English']),
			len(data['Early Modern English']),
			bool(len(data['Old English'])) + bool(len(data['Middle English'])) + bool(len(data['Early Modern English'])),
			morph,
		])

	df = pd.DataFrame(table, columns=header)
	df.to_csv('/Users/jon/Desktop/lexemes.csv')

eml = parse_celex_emw(ROOT / '..' / 'wp1' / 'data' / 'celex2' / 'english' / 'eml' / 'eml.cd')

kathy_spreadsheet()


