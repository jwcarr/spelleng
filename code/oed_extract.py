from collections import defaultdict
from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup, NavigableString
from utils import json_read


ROOT = Path(__file__).parent.parent.resolve()

DATE_REGEX = re.compile(r'^((e|l)?OE)|^((c|a|\?c|\?a)?(?P<year>\d{3,4}))')
WORD_REGEX = re.compile(r'[abcdefghijklmnopqrstuvwxyzæðþęłȝꝥ]+', re.IGNORECASE)
HEADER_EXCLUSIONS = re.compile(r'(plural|genitive|dative)', re.IGNORECASE)
NOTE_EXCLUSIONS = re.compile(r'(error|plural|genitive|dative|inflected)', re.IGNORECASE)
VARIANT_FORM_PARSER = re.compile(r'=\[(?P<form>.+?)\]=(\s\((?P<note>.+?)\))?')

HEADERS = {
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15',
}

BROAD_BANDS = {
	( 800, 1150): 'Old English',
	(1150, 1500): 'Middle English',
	(1500, 1710): 'Early Modern English',
	(1710, 2000): 'Late Modern English',
}

NARROW_BANDS = {
	( 800,  850): "Old English (I)",
	( 850,  950): "Old English (II)",
	( 950, 1050): "Old English (III)",
	(1050, 1150): "Old English (IV)",
	(1150, 1250): "Middle English (I)",
	(1250, 1350): "Middle English (II)",
	(1350, 1420): "Middle English (III)",
	(1420, 1500): "Middle English (IV)",
	(1500, 1570): "Early Modern English (I)",
	(1570, 1640): "Early Modern English (II)",
	(1640, 1710): "Early Modern English (III)",
	(1710, 1800): "Late Modern English (I)",
	(1800, 1900): "Late Modern English (II)",
	(1900, 2000): "Late Modern English (III)",
}

def normalize_date(text_date):
	if date_extract := DATE_REGEX.match(text_date):
		try:
			return int(date_extract['year'])
		except:
			if date_extract[0] == 'eOE':
				return 800
			if date_extract[0] == 'OE':
				return 900
			if date_extract[0] == 'lOE':
				return 1000
			print(f'Could not normalize date "{text_date}"')
			return None


class OEDLemma:

	def __init__(self, lemma_id):
		self.periods = []
		self.lemma_id = lemma_id
		self.lemma_file = ROOT / 'data' / 'oed' / f'{lemma_id}.html'
		if not self.lemma_file.exists():
			self.lemma_page = self.download_lemma_page()
		else:
			self.lemma_page = self.open_lemma_page()
		self.variants = self.extract_variants()
		print(self.variants)
		self.quotes = self.extract_quotes()
		

	def download_lemma_page(self):
		url = f'https://www.oed.com/dictionary/{self.lemma_id}'
		req = requests.get(url, headers=HEADERS)
		with open(self.lemma_file, 'w') as file:
			file.write(req.text)
		return BeautifulSoup(req.text, 'lxml')

	def open_lemma_page(self):
		with open(self.lemma_file) as file:
			text = file.read()
		return BeautifulSoup(text, 'lxml')

	def extract_variant_forms_table(self, variant_section):
		variants = []
		table = variant_section.find('ol')
		for table_row in table.find_all('li'):
			start = int(table_row['data-start-date'])
			if start == 950:
				start = 800
			end = int(table_row['data-end-date'])
			for variant in table_row.find_all('span', class_='variant-form'):
				variant.string.replace_with(f'=[{variant.text}]=')
			for candidate in VARIANT_FORM_PARSER.finditer(table_row.text):
				if candidate['note'] and NOTE_EXCLUSIONS.search(candidate['note']):
					continue
				if WORD_REGEX.fullmatch(candidate['form']):
					variants.append((candidate['form'], start, end))
		return variants

	def extract_variant_forms_text(self, variant_section):
		start = 800
		end = 2100
		variants = []
		for variant in variant_section.find_all('span', class_='variant-form'):
			variant.string.replace_with(f'=[{variant.text}]=')
		for candidate in VARIANT_FORM_PARSER.finditer(variant_section.text):
			if candidate['note'] and NOTE_EXCLUSIONS.search(candidate['note']):
				continue
			if WORD_REGEX.fullmatch(candidate['form']):
				variants.append((candidate['form'], start, end))
		return variants

	def extract_variant_forms(self, variant_section):
		try:
			return self.extract_variant_forms_table(variant_section)
		except:
			return self.extract_variant_forms_text(variant_section)

	def extract_variants(self):
		variants = []
		variant_section = self.lemma_page.find('section', id='variant-forms')

		variant_subsections = variant_section.find_all('div', class_='variant-forms-subsection-v1')
		if not variant_subsections:
			variant_subsections = variant_section.find_all('div', class_='variant-forms-subsection-v2')
		if not variant_subsections:
			variant_subsections = variant_section.find_all('div', class_='variant-forms-subsection-v3')

		if not variant_subsections:
			variants.extend(self.extract_variant_forms(variant_section))
		else:
			for variant_subsection in variant_subsections:
				header = variant_subsection.find(('h4', 'h5', 'h6'), class_='variant-forms-subsection-header')
				if header and HEADER_EXCLUSIONS.search(header.text):
					# print('IGNORE', header.text)
					continue

				variant_subsubsections = variant_subsection.find_all('div', class_='variant-forms-subsection-v1sub')
				if not variant_subsubsections:
					variant_subsubsections = variant_subsection.find_all('div', class_='variant-forms-subsection-v2')
				if not variant_subsubsections:
					variant_subsubsections = variant_subsection.find_all('div', class_='variant-forms-subsection-v3')
					

				if not variant_subsubsections:
					variants.extend(self.extract_variant_forms(variant_subsection))
				else:
					for variant_subsubsection in variant_subsubsections:
						header = variant_subsubsection.find(('h4', 'h5', 'h6'), class_='variant-forms-subsection-header')
						if header and HEADER_EXCLUSIONS.search(header.text):
							# print('IGNORE - ', header.text)
							continue
						variants.extend(self.extract_variant_forms(variant_subsubsection))
						
		return sorted(list(set(variants)))

	def match_quote_to_variant(self, quote, date, keyword):
		for variant, start, end in self.variants:
			variant_re = re.compile(r'\b' + variant + r'\b', re.IGNORECASE)
			if variant_re.search(keyword):
				if date >= start and date <= end:
					return variant
		return None

	def extract_quotes(self):
		variant_quote_map = defaultdict(list)
		quotation_dates = self.lemma_page.find_all('div', class_='quotation-date')
		quotation_bodies = self.lemma_page.find_all('div', class_='quotation-body')
		for date, body in zip(quotation_dates, quotation_bodies):
			date = normalize_date(date.text)
			if date is None:
				continue
			try:
				quote = body.find('blockquote').text
			except:
				continue
			try:
				keyword = body.find('mark').text
			except:
				continue

			variant = self.match_quote_to_variant(quote, date, keyword)
			if variant:
				variant_quote_map[variant].append((date, quote))

		return variant_quote_map

	def classify_band(self, date):
		for (start, end), band in BROAD_BANDS.items():
			if date >= start and date < end:
				return band
		return None

	def classify(self):
		data = {band: {f: 0 for f, s, e in self.variants} for period, band in BROAD_BANDS.items()}
		for variant, quotes in self.quotes.items():
			for date, quote in quotes:
				band = self.classify_band(date)
				if band:
					data[band][variant] += 1
		return data





if __name__ == '__main__':

	page = '''<!DOCTYPE HTML>
<html lang='en'>
<head>
<meta charset='utf-8' />
<title>OED Analysis</title>
</head>
<body>'''

	lexemes = ['man_n1', 'god_n', 'duke_n', 'king_n', 'lord_n', 'father_n', 'place_n1', 'brother_n', 'world_n', 'house_n1', 'child_n', 'woman_n', 'body_n', 'water_n', 'time_n', 'work_n', 'folk_n', 'word_n', 'grace_n', 'name_n', 'bishop_n', 'wife_n', 'life_n', 'son_n1', 'earth_n1', 'daughter_n', 'matter_n1', 'lady_n', 'master_n1', 'hand_n', 'knight_n', 'love_n1', 'church_n1', 'night_n', 'heart_n', 'mercy_n', 'power_n1']


	# lexemes = ['life_n']


	lemma_map = json_read('../data/lemma_map.json')

	periods = []
	
	for lexeme in lexemes[:]:

		print(lexeme)

		page += f'<h2>{lexeme}</h2>'

		table = '<table>\n'

		headword = lexeme.split('_')[0]
		hel_data = lemma_map[headword]

		lemma = OEDLemma(lexeme)
		oed_data = lemma.classify()

		periods.extend(lemma.periods)

		for period in ['Old English', 'Middle English', 'Early Modern English']:

			table += f'<tr><td colspan=3 style="line-height: 40px"><i>{period}</i></td></tr>\n'

			combined_forms = sorted(list(set(list(hel_data[period].keys()) + list(oed_data[period].keys()))))
			for form in combined_forms:
				try:
					hel_c = hel_data[period].get(form, '')
				except KeyError:
					hel_c = ''
				try:
					oed_c = oed_data[period].get(form, '✘')
				except KeyError:
					oed_c = ''

				table += f'<tr><td>{form}</td><td>{hel_c}</td><td>{oed_c}</td></tr>\n'


		table += '</table>\n'
		page += table

		page += '''
		</body>
		</html>
		'''

		print('------------------------------------')

	with open('/Users/jon/Desktop/output.html', 'w') as file:
		file.write(page)

	with open('../data/periods.json', 'w') as file:
		file.write(str(set(periods)))
