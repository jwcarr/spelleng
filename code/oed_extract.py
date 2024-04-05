from pathlib import Path
from collections import defaultdict
from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup
import utils


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'


DATE_REGEX = re.compile(r'^\[?(?P<period>(e|l)?OE)|^\[?(?P<year_with_approximator>(c|a|\?c|\?a)?\??(?P<year>\d{4}))')
WORD_REGEX = re.compile(r'[abcdefghijklmnopqrstuvwxyzæðþęłȝꝥ]+', re.IGNORECASE)
HEADER_EXCLUSIONS = re.compile(r'(error|plural|genitive|dative|abbreviation|2nd|3rd|participle|past|comparative|superlative|infinitive|subjunctive|imperative)', re.IGNORECASE)
NOTE_EXCLUSIONS = re.compile(r'(error|sic|plural|accusative|genitive|dative|inflected|participle|comparative|superlative|past|infinitive|subjunctive|imperative|2nd|3rd|adverb)', re.IGNORECASE)
VARIANT_FORM_PARSER = re.compile(r'=\[(?P<form>.+?)\]=(\s\((?P<note>.+?)\))?')


HTTP_REQUEST_HEADERS = {
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15',
}


class UnauthorizedAccess(Exception):
	pass

class NoEntry(Exception):
	pass


class OEDLemmaParser:

	def __init__(self, lemma_id, show_warnings=False):
		self.lemma_id = lemma_id
		self.show_warnings = show_warnings
		self.lemma_html_path = DATA / 'oed_cache' / f'{self.lemma_id}.html'
		self.lemma_json_path = DATA / 'oed_quotations' / f'{self.lemma_id}.json'

	def access(self):
		'''
		If the HTML path exists, we already have the page downloaded, so open
		it directly. Otherwise, download the page from the OED website.
		'''
		if self.lemma_html_path.exists():
			self.lemma_page = self._open_lemma_page()
		else:
			self.lemma_page = self._download_lemma_page()

	def parse(self):
		'''
		Parse the OED page.
		'''
		self.variants = self._extract_variants()
		variant_forms = [v[0] for v in self.variants]
		variant_forms.sort(key=lambda v: len(v), reverse=True)
		self.any_variant_re = re.compile(r'\b(' + '|'.join(variant_forms) + r')\b', re.IGNORECASE)
		self.quotations = self._extract_quotations()
		self.variants_to_quotations = self._create_mapping()

	def save(self):
		utils.json_write(self.variants_to_quotations, self.lemma_json_path)

	def _log(self, log_string):
		with open(DATA / 'oed_extract_log.txt', 'a') as file:
			file.write(log_string + '\n')

	def _download_lemma_page(self):
		'''
		Download the lemma's webpage from the OED and store a copy in the
		output_dir. Return the BeautifulSoup parsing of the HTML.
		'''
		url = f'https://www.oed.com/dictionary/{self.lemma_id}'
		req = requests.get(url, headers=HTTP_REQUEST_HEADERS)
		if req.status_code == 404:
			req = requests.get(url + '1', headers=HTTP_REQUEST_HEADERS)
		if req.status_code != 200:
			raise NoEntry('No entry found')
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
				if candidate['note']:
					self._log(f'tablenote > {candidate["note"]}')
				if candidate['form'].endswith('(e'):
					form_without_e = candidate['form'][:-2]
					form_with_e = candidate['form'][:-2] + 'e'
					candidate_forms = [form_without_e, form_with_e]
				else:
					candidate_forms = [candidate['form']]
				for candidate_form in candidate_forms:
					if WORD_REGEX.fullmatch(candidate_form):
						variants.append((candidate_form.lower(), start, end))
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
				if variant.string is not None:
					variant.string.replace_with(f'=[{variant.text}]=')
			section_text = section.text.replace('=[=[', '=[').replace(']=]=', ']=') # handle SIR_N
			for candidate in VARIANT_FORM_PARSER.finditer(section_text):
				if candidate['note'] and NOTE_EXCLUSIONS.search(candidate['note']):
					continue
				if candidate['note']:
					self._log('textnote > {candidate["note"]}')
				if candidate['form'].endswith('(e'):
					form_without_e = candidate['form'][:-2]
					form_with_e = candidate['form'][:-2] + 'e'
					candidate_forms = [form_without_e, form_with_e]
				else:
					candidate_forms = [candidate['form']]
				for candidate_form in candidate_forms:
					if WORD_REGEX.fullmatch(candidate_form):
						variants.append((candidate_form.lower(), start, end))
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
		Recursively expore the variant-forms part of the OED page to find
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
			if header:
				self._log(f'headernote > {header.text}')
			self._extract_variants_recursive(subsection)

	def _include_lemma_form_if_not_listed_as_variant(self):
		'''
		If the lemma headword form was not extracted from the variant forms
		section, make sure it is included.
		'''
		lemma_form = self.lemma_id.split('_')[0]
		for variant, start, end in self._temp_variants:
			if variant == lemma_form:
				return
		self._temp_variants.append((lemma_form, 800, 2000))

	def _extract_variants(self):
		'''
		Extract variant forms from the variant-forms part of the OED page.
		Then take the unique set and compile a regex for each one.
		'''
		self._temp_variants = []
		variant_section = self.lemma_page.find('section', id='variant-forms')
		if variant_section is not None:
			self._extract_variants_recursive(variant_section)
		self._include_lemma_form_if_not_listed_as_variant()
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
				year = int(date_extract['year'])
				if 'a' in date_extract['year_with_approximator']:
					year -= 10 # subtract 10 years if described as "ante"
				return year
			except:
				if date_extract['period'] == 'eOE':
					return 850
				if date_extract['period'] == 'OE':
					return 950
				if date_extract['period'] == 'lOE':
					return 1050
		if self.show_warnings:
			print(f'  Could not normalize date "{text_date}"')
		return None

	def _extract_quotation(self, quote_body):
		try:
			return quote_body.find('blockquote').text
		except:
			return None

	def _extract_keyword(self, quote_body):
		try:
			return quote_body.find('mark').text
		except:
			candidate_keywords = list(set(self.any_variant_re.findall(quote_body.text)))
			if len(candidate_keywords) == 1:
				return candidate_keywords[0]
			return None

	def _extract_quotations(self):
		'''
		Find all quotations on the OED entry page. For each one, attempt to
		(a) normalize the date, (b) extract the quotation text, and
		(c) extract the used form. If all three are extracted
		successfully, store the quote.
		'''
		quotes = set()
		quotation_dates = self.lemma_page.find_all('div', class_='quotation-date')
		quotation_bodies = self.lemma_page.find_all('div', class_='quotation-body')
		assert len(quotation_dates) == len(quotation_bodies)
		for date, body in zip(quotation_dates, quotation_bodies):
			if year := self._normalize_date_to_year(date.text):
				if quote := self._extract_quotation(body):
					if keyword := self._extract_keyword(body):
						quotes.add((year, keyword, quote))
		return list(quotes)

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


def main(lemmata_file, delay=0, show_warnings=False, access_only=False):
	from time import sleep

	lemmata = utils.json_read(lemmata_file)

	# remove this section ##########
	lemmata = list(lemmata.keys())
	lemmata.reverse()
	# from random import shuffle
	# shuffle(lemmata)
	# remove this section ##########

	for i, lemma in enumerate(lemmata, 1):

		# sleep(delay)
		
		# print(i, lemma)

		# remove this section ##########
		# if (DATA / 'oed_quotations' / f'{lemma}.json').exists():
		# 	continue
		print(i, lemma)
		if not (DATA / 'oed_cache' / f'{lemma}.html').exists():
			continue
		# remove this section #########

		oed_lemma_parser = OEDLemmaParser(lemma, show_warnings=show_warnings)

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
			continue

		oed_lemma_parser.save()


if __name__ == '__main__':

	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('lemmata_file', action='store', type=str, help='json file listing lemmata to extract/parse')
	parser.add_argument('--delay', action='store', type=int, default=0, help='delay (in seconds) between each lemma extraction/parsing')
	parser.add_argument('--warnings', action='store_true', help='show parser warnings')
	parser.add_argument('--access_only', action='store_true', help='show parser warnings')
	args = parser.parse_args()

	main(
		args.lemmata_file,
		delay=args.delay,
		show_warnings=args.warnings,
		access_only=args.access_only,
	)
