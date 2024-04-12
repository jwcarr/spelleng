from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup
import utils


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'
OED_CACHE_DIR = DATA / 'oed_cache'


DATE_REGEX = re.compile(r'^\[?(?P<period>(e|l)?OE)|^\[?(?P<year_with_approximator>(c|a|\?c|\?a)?\??(?P<year>\d{4}))')
WORD_REGEX = re.compile(r'[abcdefghijklmnopqrstuvwxyzæðþęłȝꝥ]+', re.IGNORECASE)
HEADER_EXCLUSIONS = re.compile(r'(error|plural|genitive|dative|abbreviation|2nd|3rd|participle|past|comparative|superlative|infinitive|subjunctive|imperative)', re.IGNORECASE)
NOTE_EXCLUSIONS = re.compile(r'(error|sic|plural|accusative|genitive|dative|inflected|participle|comparative|superlative|past|infinitive|subjunctive|imperative|2nd|3rd|adverb)', re.IGNORECASE)
VARIANT_FORM_PARSER = re.compile(r'=\[(?P<form>.+?)\]=(\s\((?P<note>.+?)\))?', re.IGNORECASE)
OPTIONAL_LETTERS = re.compile(r'-?\w*\((?P<letter>\w)\)\w*', re.IGNORECASE)
OPTIONAL_FINAL_LETTER = re.compile(r'\([a-z]$', re.IGNORECASE)

ALT_SUFFIX_FORMS = utils.json_read(DATA / 'alt_suffix_forms.json')
MANUAL_INCLUSIONS = utils.json_read(DATA / 'manual_inclusions.json')
MANUAL_EXCLUSIONS = utils.json_read(DATA / 'manual_exclusions.json')

HTTP_REQUEST_HEADERS = {
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15',
}

OED_MAPPING_OVERRIDE = {'firm_n': 'firm_n2'}


class UnauthorizedAccess(Exception):
	pass

class NoEntry(Exception):
	pass

class NoVariantForms(Exception):
	pass

class OEDLemmaParser:

	def __init__(self, lemma_id, show_warnings=False):
		self.lemma_id = lemma_id
		self.show_warnings = show_warnings
		self.lemma_html_path = OED_CACHE_DIR / f'{self.lemma_id}.html'
		self.variants_to_quotations = {}
		self.headword_form, self.pos = self.lemma_id.split('_')
		self.manual_inclusions = MANUAL_INCLUSIONS.get(lemma_id, [])
		self.manual_exclusions = MANUAL_EXCLUSIONS.get(lemma_id, [])

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
		self.variant_rejector = self._create_variant_rejector()
		self.variants = self._extract_variants()
		variant_forms = [v[0] for v in self.variants]
		variant_forms.sort(key=lambda v: len(v), reverse=True)
		self.any_variant_re = re.compile(r'\b(' + '|'.join(variant_forms) + r')\b', re.IGNORECASE)
		self.quotations = self._extract_quotations()
		self.variants_to_quotations = self._create_mapping()

	def save(self, output_dir):
		output_file = output_dir / f'{self.lemma_id}.json'
		utils.json_write(self.variants_to_quotations, output_file)

	def _log(self, log_string):
		with open(DATA / 'oed_extract_log.txt', 'a') as file:
			file.write(log_string + '\n')

	def _download_lemma_page(self):
		'''
		Download the lemma's webpage from the OED and store a copy in the
		output_dir. Return the BeautifulSoup parsing of the HTML.
		'''
		if self.lemma_id in OED_MAPPING_OVERRIDE:
			url = f'https://www.oed.com/dictionary/{OED_MAPPING_OVERRIDE[self.lemma_id]}'
		else:
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

	def _create_variant_rejector(self):
		'''
		Depending on the part of speech and characteristics of the headword
		form, create a regular expression to catch modern inflected forms
		that should be rejected.
		'''
		if self.pos == 'n':
			if self.headword_form.endswith('us'): # Latin masculine
				return re.compile(r'\b(' + self.headword_form[:-2] + r'i|' + self.headword_form + r'es)\b')
			elif self.headword_form.endswith('a'): # Latin feminine
				return re.compile(r'\b(' + self.headword_form + r'e|' + self.headword_form + r's)\b')
			elif self.headword_form.endswith('um'): # Latin neuter
				return re.compile(r'\b(' + self.headword_form[:-2] + r'a|' + self.headword_form + r's)\b')
			elif self.headword_form.endswith('on'): # Greek neuter
				return re.compile(r'\b(' + self.headword_form[:-2] + r'a|' + self.headword_form + r's)\b')
			elif self.headword_form.endswith(('ch', 'sh', 's', 'x', 'z')): # English -es after sibilant
				return re.compile(r'\b' + self.headword_form + r'(es)\b')
		elif self.pos == 'v':
			if self.headword_form.endswith('y'):
				return re.compile(r'\b(' + self.headword_form[:-1] + r'ied|' + self.headword_form + r'ed)\b')
			else:
				return re.compile(r'\b' + self.headword_form + r'(ing|ed)\b')
		elif self.pos == 'adj':
			if self.headword_form.endswith('e'):
				return re.compile(r'\b' + self.headword_form + r'(st|r)\b')
			else:
				return re.compile(r'\b' + self.headword_form + r'(est|er)\b')
		return None

	def _evaluate_candidate(self, candidate, start, end):
		'''
		Given a candidate variant form, expand any optional letters to prodice
		a set of cadidates, and decide whether or not each candidate
		should be accepted.
		'''
		if candidate['note'] and NOTE_EXCLUSIONS.search(candidate['note']):
			return
		if OPTIONAL_FINAL_LETTER.search(candidate['form']):
			optional_letter = candidate['form'][-1]
			form_without_optional_letter = candidate['form'][:-2]
			form_with_optional_letter = form_without_optional_letter + optional_letter
			candidate_forms = [form_without_optional_letter, form_with_optional_letter]
		else:
			candidate_forms = [candidate['form']]
		additional_candidates = []
		for candidate_form in candidate_forms:
			if optional_match := OPTIONAL_LETTERS.fullmatch(candidate_form):
				letter = optional_match['letter']
				additional_candidates.append(
					candidate_form.replace(f'({letter})', letter)
				)
				additional_candidates.append(
					candidate_form.replace(f'({letter})', '')
				)
		candidate_forms.extend(additional_candidates)
		for candidate_form in candidate_forms:
			if candidate_form.startswith('-') or candidate_form.endswith('-'):
				candidate_form = self._expand_alternate_suffix(candidate_form)
			if candidate_form in self.manual_exclusions:
				return
			if self.variant_rejector and self.variant_rejector.fullmatch(candidate_form):
				return
			if WORD_REGEX.fullmatch(candidate_form):
				self._temp_variants.append((candidate_form.lower(), start, end))

	def _extract_variant_forms_table(self, section):
		'''
		Given an OED table of variants, iterate over each row and extract the
		variants and time period during which those variants are attested.
		Any notes provided alongide a variant (i.e. in parentheses) are
		also extracted.
		'''
		table = section.find('ol')
		for table_row in table.find_all('li'):
			start = int(table_row['data-start-date'])
			if start == 950:
				start = 800 # OED variants from "Old English" have a start of 950, but early dates should also be Old English
			end = int(table_row['data-end-date'])
			for variant in table_row.find_all('span', class_='variant-form'):
				variant.string.replace_with(f'=[{variant.text}]=')
			for candidate in VARIANT_FORM_PARSER.finditer(table_row.text):
				self._evaluate_candidate(candidate, start, end)

	def _extract_variant_forms_text(self, section):
		'''
		Given an OED sentence style description of variants, extract the
		variants and any associated notes. In these cases, it is difficult
		to parse the time period that applies to a given variant, so we
		just assume that each variant covers the entire 800-2000 period
		and rely on the quotations to date things.
		'''
		for x in section.text.split('.'):
			print(x.strip())
		start, end = 800, 2000
		if candidate_variants := section.find_all('span', class_='variant-form'):
			for variant in candidate_variants:
				if variant.string is not None:
					variant.string.replace_with(f'=[{variant.text}]=')
			section_text = section.text.replace('=[=[', '=[').replace(']=]=', ']=') # handle SIR_N
			for candidate in VARIANT_FORM_PARSER.finditer(section_text):
				self._evaluate_candidate(candidate, start, end)

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
			return self._extract_variant_forms(section)
		for subsection in subsections:
			header = subsection.find(('h4', 'h5', 'h6'), class_='variant-forms-subsection-header')
			if header and HEADER_EXCLUSIONS.search(header.text):
				continue
			self._extract_variants_recursive(subsection)

	def _include_headword_form_if_not_listed_as_variant(self):
		'''
		If the lemma headword form was not extracted from the variant forms
		section, make sure it is included.
		'''
		for variant, start, end in self._temp_variants:
			if variant == self.headword_form:
				return
		self._temp_variants.append((self.headword_form, 800, 2000))

	def _include_manual_inclusions(self):
		'''
		Include any manual inclusions.
		'''
		for manual_inclusion_form in self.manual_inclusions:
			self._temp_variants.append((manual_inclusion_form, 800, 2000))

	def _expand_alternate_suffix(self, candidate_form):
		'''
		If the OED lists a variant spelling like "-acoun" for a word
		like "consideration", expand the variant to its full form
		(i.e., "consideracion"). To do this, we take the first letter of
		the variant suffix (e.g. "a") and find the last occurance on
		an "a" in the headword form and make the replacement.
		'''
		if candidate_form.startswith('-'):
			alt_suffix = candidate_form[1:]
		else:
			alt_suffix = candidate_form[:-1]
		try:
			return re.sub(ALT_SUFFIX_FORMS[candidate_form], alt_suffix, self.headword_form)
		except Exception:
			return candidate_form

	def _extract_variants(self):
		'''
		Extract variant forms from the variant-forms part of the OED page.
		Then take the unique set and compile a regex for each one.
		'''
		self._temp_variants = []
		variant_section = self.lemma_page.find('section', id='variant-forms')
		if variant_section is None:
			raise NoVariantForms('No variant forms section')
		self._extract_variants_recursive(variant_section)
		self._include_headword_form_if_not_listed_as_variant()
		self._include_manual_inclusions()
		if len(self._temp_variants) <= 1:
			raise NoVariantForms('No variant forms found')
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
		for editorial_comment in self.lemma_page.find_all(class_='editorial-comment'):
			editorial_comment.extract() # remove any editorial comments from the quotations
		quotes = set()
		quotation_dates = self.lemma_page.find_all('div', class_='quotation-date')
		quotation_bodies = self.lemma_page.find_all('div', class_='quotation-body')
		assert len(quotation_dates) == len(quotation_bodies)
		for date, body in zip(quotation_dates, quotation_bodies):
			# if 'Corinthe' in body.text:
			# 	print(1, body.text)
			if year := self._normalize_date_to_year(date.text):
				# if 'Corinthe' in body.text:
				# 	print(2, year)
				if quote := self._extract_quotation(body):
					# if 'Corinthe' in body.text:
					# 	print(3, quote)
					if keyword := self._extract_keyword(body):
						# if 'Corinthe' in body.text:
						# 	print(4, year, keyword, quote)
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
			if year >= (start - 70) and year <= (end + 70) and variant_re.search(keyword):
				return variant
		return None

	def _create_mapping(self):
		'''
		Map each extracted quote onto an extracted variant.
		'''
		variant_quote_map = {variant: [] for variant, s, e, v in self.variants}
		for year, keyword, quote in self.quotations:
			# if 'Corinthe' in quote:
			# 	print(5, year, keyword, quote)
			if variant := self._map_quote_to_variant(year, keyword, quote):
				# if 'Corinthe' in quote:
				# 	print(6, variant, quote)
				variant_quote_map[variant].append((year, quote))
		for quotes in variant_quote_map.values():
			quotes.sort()
		return variant_quote_map


def main(lemmata_file, output_dir, parse_only=False, show_warnings=False, start_from=None, stop_at=None):
	
	if not output_dir.exists():
		output_dir.mkdir()
	
	lemmata = list(utils.json_read(lemmata_file).keys())
	
	if start_from is None:
		start_from = 0
	if stop_at is None:
		stop_at = len(lemmata)
	
	for lemma_i in range(start_from, stop_at):
		lemma = lemmata[lemma_i]

		if parse_only and not (OED_CACHE_DIR / f'{lemma}.html').exists():
			continue
		
		print(lemma_i, lemma)
		
		oed_lemma_parser = OEDLemmaParser(lemma, show_warnings=show_warnings)

		try:
			oed_lemma_parser.access()
		except UnauthorizedAccess:
			print('Access to OED not authorized; stopping.')
			break
		except Exception as e:
			print(f'- Failed to access {lemma}; continuing...')

		try:
			oed_lemma_parser.parse()
		except NoVariantForms:
			continue
		except Exception:
			print(f'- Failed to parse {lemma}; continuing...')
			continue

		oed_lemma_parser.save(output_dir)


if __name__ == '__main__':

	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('lemmata_file', action='store', type=str, help='json file listing lemmata to extract/parse')
	parser.add_argument('output_dir', action='store', type=str, help='directory to store json output for each lemma')
	parser.add_argument('--parse_only', action='store_true', help='do not attempt to download if unavailable')
	parser.add_argument('--warnings', action='store_true', help='show parser warnings')
	parser.add_argument('--start', action='store', type=int, help='lemma number to start from')
	parser.add_argument('--stop', action='store', type=int, help='lemma number to stop at')
	args = parser.parse_args()

	main(
		Path(args.lemmata_file),
		Path(args.output_dir),
		parse_only=args.parse_only,
		show_warnings=args.warnings,
		start_from=args.start,
		stop_at=args.stop,
	)
