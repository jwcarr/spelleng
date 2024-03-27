from collections import defaultdict
from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup
from utils import json_write


DATE_REGEX = re.compile(r'^((e|l)?OE)|^((c|a|\?c|\?a)?\??(?P<year>\d{3,4}))')
WORD_REGEX = re.compile(r'[abcdefghijklmnopqrstuvwxyzæðþęłȝꝥ]+', re.IGNORECASE)
HEADER_EXCLUSIONS = re.compile(r'(plural|genitive|dative|abbreviation)', re.IGNORECASE)
NOTE_EXCLUSIONS = re.compile(r'(error|plural|genitive|dative|inflected)', re.IGNORECASE)
VARIANT_FORM_PARSER = re.compile(r'=\[(?P<form>.+?)\]=(\s\((?P<note>.+?)\))?')


HTTP_REQUEST_HEADERS = {
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15',
}


class UnauthorizedAccess(Exception):
	pass


class OEDLemmaParser:

	def __init__(self, lemma_id, output_dir, show_warnings=False):
		self.lemma_id = lemma_id
		self.show_warnings = show_warnings
		self.lemma_html_path = output_dir / f'{self.lemma_id}.html'
		self.lemma_json_path = output_dir / f'{self.lemma_id}.json'

	def access(self):
		'''
		If the HTML path exists, we already have the page downloaded, so open
		it directly. Otherwise, download the page from the OED website.
		'''
		if self.lemma_html_path.exists():
			self.lemma_page = self._open_lemma_page()
		self.lemma_page = self._download_lemma_page()

	def parse(self):
		'''
		Parse the OED page.
		'''
		self.variants = self._extract_variants()
		self.quotations = self._extract_quotations()
		self.variants_to_quotations = self._create_mapping()

	def save(self):
		json_write(self.variants_to_quotations, self.lemma_json_path)

	def _download_lemma_page(self):
		'''
		Download the lemma's webpage from the OED and store a copy in the
		output_dir. Return the BeautifulSoup parsing of the HTML.
		'''
		url = f'https://www.oed.com/dictionary/{self.lemma_id}'
		req = requests.get(url, headers=HTTP_REQUEST_HEADERS)
		lemma_page = BeautifulSoup(req.text, 'lxml')
		if lemma_page.find('div', class_='paywallOptions'):
			raise UnauthorizedAccess('No access to OED')
		with open(self.lemma_html_path, 'w') as file:
			file.write(req.text)
		return lemma_page

	def _open_lemma_page(self):
		'''
		Open the saved webpage and return the BeautifulSoup parsing of the HTML.
		'''
		with open(self.lemma_html_path) as file:
			text = file.read()
		return BeautifulSoup(text, 'lxml')

	def _extract_variant_forms_table(self, section):
		'''
		Given an OED table of variants, iterate over each row and extract the
		variants and time period during which those variants are attested.
		Any notes provided alongide a variant (i.e. in parentheses) are
		also extracted; if the notes contain banned terms (e.g. "genitive"),
		the variant is ignored.
		'''
		variants = []
		table = section.find('ol')
		for table_row in table.find_all('li'):
			start = int(table_row['data-start-date'])
			if start == 950:
				start = 800 # OED variants from "Old English" have a start of 950, but early dates should also be Old English
			end = int(table_row['data-end-date'])
			for variant in table_row.find_all('span', class_='variant-form'):
				variant.string.replace_with(f'=[{variant.text}]=')
			for candidate in VARIANT_FORM_PARSER.finditer(table_row.text):
				if candidate['note'] and NOTE_EXCLUSIONS.search(candidate['note']):
					continue
				if WORD_REGEX.fullmatch(candidate['form']):
					variants.append((candidate['form'], start, end))
		return variants

	def _extract_variant_forms_text(self, section):
		'''
		Given an OED sentence style description of variants, extract the
		variants and any associated notes. In these cases, it is difficult
		to parse the time period that applies to a given variant, so we
		just assume that each variant covers the entire 800-2000 period
		and rely on the quotations to date things.
		'''
		variants = []
		start, end = 800, 2000
		if candidate_variants := section.find_all('span', class_='variant-form'):
			for variant in candidate_variants:
				variant.string.replace_with(f'=[{variant.text}]=')
			for candidate in VARIANT_FORM_PARSER.finditer(section.text):
				if candidate['note'] and NOTE_EXCLUSIONS.search(candidate['note']):
					continue
				if WORD_REGEX.fullmatch(candidate['form']):
					variants.append((candidate['form'], start, end))
		return variants

	def _extract_variant_forms(self, section):
		'''
		Each OED variant form section comes in one of two formats: a tabular
		format or a flat text format. First we try to parse the section as
		a table, but if this fails, we fall back on parsing it as text.
		'''
		try:
			return self._extract_variant_forms_table(section)
		except:
			return self._extract_variant_forms_text(section)

	def _extract_variants_recursive(self, section):
		'''
		Recursively expore the varient-forms part of the OED page to find
		candidate sections that may contain variants. So long as the
		section header does not contain an excluded term (e.g. "genitive"),
		pass the section to _extract_variant_forms().
		'''
		subsections = section.find_all('div', class_='variant-forms-subsection-v1')
		if not subsections:
			subsections = section.find_all('div', class_='variant-forms-subsection-v1sub')
		if not subsections:
			subsections = section.find_all('div', class_='variant-forms-subsection-v2')
		if not subsections:
			subsections = section.find_all('div', class_='variant-forms-subsection-v3')
		if not subsections:
			return self._temp_variants.extend(self._extract_variant_forms(section))
		for subsection in subsections:
			header = subsection.find(('h4', 'h5', 'h6'), class_='variant-forms-subsection-header')
			if header and HEADER_EXCLUSIONS.search(header.text):
				continue
			self._extract_variants_recursive(subsection)

	def _extract_variants(self):
		'''
		Extract variant forms from the varient-forms part of the OED page.
		Then take the unique set and compile a regex for each one.
		'''
		self._temp_variants = []
		variant_section = self.lemma_page.find('section', id='variant-forms')
		self._extract_variants_recursive(variant_section)
		return [
			(variant, start, end, re.compile(r'\b' + variant + r'\b', re.IGNORECASE))
			for variant, start, end in sorted(list(set(self._temp_variants)))
		]

	def _normalize_date_to_year(self, text_date):
		'''
		Given a quotation date in text format, try to turn that date into an
		integer. Returns None if the date cannot be determined.
		'''
		if date_extract := DATE_REGEX.match(text_date):
			try:
				return int(date_extract['year'])
			except:
				if date_extract[0] == 'eOE':
					return 850
				if date_extract[0] == 'OE':
					return 950
				if date_extract[0] == 'lOE':
					return 1050
		return None

	def _extract_quotations(self):
		'''
		Find all quotations on the OED entry page. For each one, attempt to
		(a) normalize the date, (b) extract the quotation text, and
		(c) extract the used form. If all three are extracted
		successfully, store the quote.
		'''
		quotes = []
		quotation_dates = self.lemma_page.find_all('div', class_='quotation-date')
		quotation_bodies = self.lemma_page.find_all('div', class_='quotation-body')
		for date, body in zip(quotation_dates, quotation_bodies):
			year = self._normalize_date_to_year(date.text)
			if year is None:
				if self.show_warnings:
					print(f'  Could not normalize date "{date.text}"')
				continue
			try:
				quote = body.find('blockquote').text
				keyword = body.find('mark').text
			except:
				if self.show_warnings:
					print(f'  Could not parse quote')
				continue
			quotes.append((year, keyword, quote))
		return quotes

	def _map_quote_to_variant(self, year, keyword, quote):
		'''
		For a given quote attested in a given year, check it against all
		variants until you find a variant that is (a) contained inside the
		keyword and (b) was attested with the variant's attested period.
		If no variant is found, return None.
		'''
		for variant, start, end, variant_re in self.variants:
			if year >= start and year <= end and variant_re.search(keyword):
				return variant
		return None

	def _create_mapping(self):
		'''
		Map each extracted quote onto an extracted variant.
		'''
		variant_quote_map = {variant: [] for variant, s, e, v in self.variants}
		for year, keyword, quote in self.quotations:
			if variant := self._map_quote_to_variant(year, keyword, quote):
				variant_quote_map[variant].append((year, quote))
		for quotes in variant_quote_map.values():
			quotes.sort()
		return variant_quote_map


def main(lemmata_file, output_dir, start_from=0, delay=0, show_warnings=False, access_only=False):
	from time import sleep

	output_dir = Path(output_dir)
	if not output_dir.exists():
		output_dir.mkdir()

	with open(lemmata_file) as file:
		lemmata = file.read()
	lemmata = lemmata.split('\n')

	for i, lemma in enumerate(lemmata[start_from:], start_from):

		sleep(delay)
		
		print(i, lemma)
		oed_lemma_parser = OEDLemmaParser(lemma, output_dir, show_warnings=show_warnings)

		try:
			oed_lemma_parser.access()
		except UnauthorizedAccess:
			print('Access to OED not authorized; stopping.')
			break
		except Exception as e:
			print(f'- Failed to access {lemma}; continuing...')

		if access_only:
			continue

		try:
			oed_lemma_parser.parse()
		except Exception as e:
			print(f'- Failed to parse {lemma}; continuing...')

		oed_lemma_parser.save()


if __name__ == '__main__':

	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('lemmata_file', action='store', type=str, help='txt file listing lemmata to extract/parse')
	parser.add_argument('output_dir', action='store', type=str, help='directory to store extracted/parsed data')
	parser.add_argument('--start', action='store', type=int, default=0, help='lemma number to start from')
	parser.add_argument('--delay', action='store', type=int, default=0, help='delay (in seconds) between each lemma extraction/parsing')
	parser.add_argument('--warnings', action='store_true', help='show parser warnings')
	parser.add_argument('--access_only', action='store_true', help='show parser warnings')
	args = parser.parse_args()

	main(args.lemmata_file, args.output_dir, args.start, args.delay, args.warnings, args.access_only)
