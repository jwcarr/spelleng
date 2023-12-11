from collections import defaultdict
from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup, NavigableString
from utils import json_read


ROOT = Path(__file__).parent.parent.resolve()

DATE_REGEX = re.compile(r'^((e|l)?OE)|^((c|a|\?c|\?a)?(?P<year>\d{3,4}))')
ENTRY_REGEX = re.compile(r'Entry/(\d+)\?')
ENTRY_REGEX = re.compile(r'/dictionary/(\w+)')
WORD_REGEX = re.compile(r'[abcdefghijklmnopqrstuvwxyzæðþęłȝꝥ]+')

HEADERS = {
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15',
}

CENTURY_BANDS = {
	'9th': (800, 900),
	'10th': (900, 1000),
	'11th': (1000, 1100),
	'12th': (1100, 1200),
	'13th': (1200, 1300),
	'14th': (1300, 1400),
	'15th': (1400, 1500),
	'16th': (1500, 1600),
	'17th': (1600, 1700),
	'18th': (1700, 1800),
	'19th': (1800, 1900),
	'20th': (1900, 2000),
}

BROAD_BANDS = {
	'Old English': (800, 1150),
	'Middle English': (1150, 1500),
	'Early Modern English': (1500, 1710),
	'Late Modern English': (1710, 2000),
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
		self.lemma_id = lemma_id
		self.lemma_file = ROOT / 'data' / 'oed' / f'{lemma_id}.html'
		if not self.lemma_file.exists():
			self.lemma_page = self.download_lemma_page()
		else:
			self.lemma_page = self.open_lemma_page()
		self.variants = self.extract_variants()
		self.variant_parser = re.compile('|'.join(sorted(self.variants, key=lambda k: len(k), reverse=True)))
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

	def extract_variants(self):
		variant_div = self.lemma_page.find('div', class_='variant-forms-subsection-v3')
		if variant_div is None:
			variant_div = self.lemma_page.find('section', id='variant-forms')
		variants = variant_div.find_all('span', class_='variant-form')
		return sorted([v.text for v in variants if WORD_REGEX.fullmatch(v.text)])

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

			form = self.variant_parser.match(keyword)
			if form is None:
				continue
			variant = form[0]

			variant_quote_map[variant].append((date, quote))
		return variant_quote_map

	def classify_band(self, date):
		for band, (start, end) in BROAD_BANDS.items():
			if date >= start and date < end:
				return band
		return None

	def classify(self):
		data = {band: defaultdict(int) for band in BROAD_BANDS.keys()}
		for variant, quotes in self.quotes.items():
			for date, quote in quotes:
				band = self.classify_band(date)
				if band:
					data[band][variant] += 1
		pprint(data)





if __name__ == '__main__':

	from pprint import pprint

	lemma = OEDLemma('heart_n')
	pprint(lemma.quotes)
	lemma.classify()




