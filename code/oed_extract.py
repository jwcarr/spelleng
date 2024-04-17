from pathlib import Path
from copy import deepcopy
import re
import requests
from bs4 import BeautifulSoup
import utils


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'
OED_CACHE_DIR = DATA / 'oed_cache'


DATE_REGEX = re.compile(r'^\[?(?P<period>(e|l)?OE)|^\[?(?P<year_with_approximator>(c|a|\?c|\?a)?\??(?P<year>\d{4}))')
WORD_REGEX = re.compile(r'[abcdefghijklmnopqrstuvwxyzæðþęłȝꝥ]+', re.IGNORECASE)
HEADER_EXCLUSIONS = re.compile(r'(chiefly in sense|error|plural|genitive|dative|abbreviation|2nd|3rd|participle|past|comparative|superlative|infinitive|subjunctive|imperative)', re.IGNORECASE)
NOTE_EXCLUSIONS = re.compile(r'(error|sic|plural|accusative|genitive|dative|inflected|participle|comparative|superlative|past|infinitive|subjunctive|imperative|2nd|3rd|adverb)', re.IGNORECASE)
VARIANT_FORM_PARSER = re.compile(r'(?P<gnote>.*?)=\[(?P<form>.+?)\]=(\s\((?P<note>.+?)\))?', re.IGNORECASE)
OPTIONAL_LETTERS = re.compile(r'-?\w*\((?P<letter>\w)\)\w*', re.IGNORECASE)
OPTIONAL_FINAL_LETTER = re.compile(r'\([a-z]$', re.IGNORECASE)
PARENTHETICAL_CLEANER = re.compile(r'(Shetland)|(Orkney)|Orm\.', re.IGNORECASE)
OED_URL_PARSER = re.compile(r'/dictionary/(?P<lemma_id>\w+_\w+)')
OED_LEMMA_MAPPER = re.compile(r'(?P<id>\w+_(adj|n|v))1?')

OED_AFFIXES = utils.json_read(DATA / 'oed_affixes.json')
ALT_SUFFIX_FORMS = utils.json_read(DATA / 'alt_suffix_forms.json')
MANUAL_INCLUSIONS = utils.json_read(DATA / 'manual_inclusions.json')
MANUAL_EXCLUSIONS = utils.json_read(DATA / 'manual_exclusions.json')

DEFAULT_ITEM = {'variant': None, 'start': 800, 'end': 2100, 'notes': ''}
PERIOD_MAP = {
	'OldEnglish': {'start': 800, 'end': 1150},
	'MiddleEnglish': {'start': 1150, 'end': 1500},
	'EarlyModernEnglish': {'start': 1500, 'end': 1710},
	'1400s': {'start': 1400, 'end': 1500},
	'1500s': {'start': 1500, 'end': 1600},
	'1600s': {'start': 1600, 'end': 1700},
	'1700s': {'start': 1700, 'end': 1800},
	'1800s': {'start': 1800, 'end': 1900},
	'1900s': {'start': 1900, 'end': 2000},
	'–1400s': {'end': 1500},
	'–1500s': {'end': 1600},
	'–1600s': {'end': 1700},
	'–1700s': {'end': 1800},
	'–1800s': {'end': 1900},
	'–1900s': {'end': 2000},
	'–': {'end': 2100}
}

HTTP_REQUEST_HEADERS = {
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15',
}

OED_MAPPING_OVERRIDE = {'firm_n': 'firm_n2'}


class UnauthorizedAccess(Exception):
	pass

class NoEntry(Exception):
	pass

class OEDLemmaParser:

	def __init__(self, lemma_id, show_warnings=False, do_not_resolve_cross_references=False):
		self.lemma_id = lemma_id
		self.show_warnings = show_warnings
		self.do_not_resolve_cross_references = do_not_resolve_cross_references
		self.lemma_html_path = OED_CACHE_DIR / f'{self.lemma_id}.html'
		self.variants_to_quotations = {}
		self.headword_form, self.pos = self.lemma_id.split('_')
		self.manual_inclusions = MANUAL_INCLUSIONS.get(lemma_id, [])
		self.manual_exclusions = MANUAL_EXCLUSIONS.get(lemma_id, [])

	################
	# PUBLIC METHODS
	################

	def access(self):
		'''
		If the HTML path exists, we already have the page downloaded, so open
		it directly. Otherwise, download the page from the OED website.
		'''
		if self.lemma_html_path.exists():
			self.lemma_page = self._open_lemma_page()
		else:
			self.lemma_page = self._download_lemma_page()

	def parse(self, drop_unattested_variants=False):
		'''
		Parse the OED page.
		'''
		self.variant_rejector = self._create_variant_rejector()
		self.variants = self._extract_variants()
		variant_forms = [v[0] for v in self.variants]
		variant_forms.sort(key=lambda v: len(v), reverse=True)
		self.any_variant_re = re.compile(r'\b(' + '|'.join(variant_forms) + r')\b', re.IGNORECASE)
		self.quotations = self._extract_quotations()
		self.variants_to_quotations = self._create_mapping(drop_unattested_variants)

	def save(self, output_dir):
		output_file = output_dir / f'{self.lemma_id}.json'
		utils.json_write(self.variants_to_quotations, output_file)

	#################
	# ACCESS OED DATA
	#################

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

	#######################
	# VARIANT FORMS PARSING
	#######################

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

	def _extract_variants(self):
		'''
		Extract variant forms from the variant-forms part of the OED page.
		Then take the unique set and compile a regex for each one.
		'''
		self._temp_variants = []
		variant_section = self.lemma_page.find('section', id='variant-forms')
		if variant_section is not None:
			self._extract_variants_recursive(variant_section)
		self._include_headword_form_if_not_listed_as_variant()
		self._include_manual_inclusions()
		return [
			(variant, start, end, re.compile(r'\b' + variant + r'\b', re.IGNORECASE))
			for variant, start, end in sorted(list(set(self._temp_variants)))
		]

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
			try:
				return self._extract_variant_forms_table(section)
			except:
				return self._extract_variant_forms_text(section)
		for subsection in subsections:
			header = subsection.find(('h4', 'h5', 'h6'), class_='variant-forms-subsection-header')
			if header and HEADER_EXCLUSIONS.search(header.text):
				continue
			self._extract_variants_recursive(subsection)

	def _extract_variant_forms_table(self, section):
		'''
		Given an OED table of variants, iterate over each row and extract the
		variants and time period during which those variants are attested.
		Any notes provided alongide a variant (i.e. in parentheses) are
		also extracted.
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
				if candidate['gnote'] and NOTE_EXCLUSIONS.search(candidate['gnote']):
					continue
				variants.apppend((candidate['form'].lower(), start, end))
		
		variants = self._expand_abbreviations(variants)
		variants = self._drop_invalid_forms(variants)
		for variant, start, end in variants:
			self._temp_variants.append((variant.lower(), start, end))

	def _extract_variant_forms_text(self, section):
		'''
		Given an OED sentence style description of variants, extract the
		variants and any associated notes. In these cases, it is difficult
		to parse the time period that applies to a given variant, so we
		just assume that each variant covers the entire 800-2000 period
		and rely on the quotations to date things.
		'''
		if header := section.find('h3'):
			header.extract() # remove "Variant Forms" header
		cross_refs = []
		for cross_ref in section.find_all('a', class_='cross-reference'):
			cross_refs.append(cross_ref.extract())
		if cross_refs and self.do_not_resolve_cross_references == False:
			self._resolve_cross_references(cross_refs)

		if candidate_variants := section.find_all('span', class_='variant-form'):
			for variant in candidate_variants:
				if variant.string is not None:
					variant.string.replace_with(f'=[{variant.text}]=')

			description_tokens = self.tokenize_description(section.text)
			variants = []
			item = deepcopy(DEFAULT_ITEM)
			first_label_set = None
			for token in description_tokens:
				if token == ',' or (token == ';' and first_label_set is None):
					if item['variant']:
						variants.append(deepcopy(item))
						item['variant'] = None
				elif token == '.' or (token == ';' and first_label_set == 'period'):
					if item['variant']:
						variants.append(deepcopy(item))
						item = deepcopy(DEFAULT_ITEM)
						first_label_set = None
				elif match := VARIANT_FORM_PARSER.match(token):
					item['variant'] = match['form']
				elif update := PERIOD_MAP.get(token, None):
					item |= update
					if first_label_set is None:
						first_label_set = 'period'
					elif first_label_set == 'period':
						item['notes'] = ''
				elif len(token) > 1:
					item['notes'] += token + ' '
					if first_label_set is None:
						first_label_set = 'note'
			
			variants = self._drop_note_exclusions(variants)
			variants = self._expand_abbreviations(variants)
			variants = self._drop_invalid_forms(variants)
			for variant, start, end in variants:
				self._temp_variants.append((variant.lower(), start, end))

	def tokenize_description(self, description):
		description = description.replace(',', ' , ')
		description = description.replace('.', ' . ')
		description = description.replace('=[', ' =[')
		description = description.replace(']=', ']= ')
		description = description.replace('–', ' –')
		description = re.sub(r'\/.+?\/', '', description) # remove IPA transcriptions
		description = description.replace('Old English', ' OldEnglish ' )
		description = description.replace('Middle English', ' MiddleEnglish ' )
		description = description.replace('Early Modern English', ' EarlyModernEnglish ' )
		description = re.sub(r'\s+', ' ', description) # remove multiple consecutive spaces
		return description.split(' ')

	def _drop_note_exclusions(self, variants):
		new_variants = []
		for variant in variants:
			if NOTE_EXCLUSIONS.search(variant['notes']):
				continue
			new_variants.append((variant['variant'], variant['start'], variant['end']))
		return new_variants

	def _expand_abbreviations(self, variants1):
		variants2 = []
		for variant, start, end in variants1:
			if OPTIONAL_FINAL_LETTER.search(variant):
				optional_letter = variant[-1]
				form_without_optional_letter = variant[:-2]
				form_with_optional_letter = form_without_optional_letter + optional_letter
				variants2.append((form_without_optional_letter, start, end))
				variants2.append((form_with_optional_letter, start, end))
			else:
				variants2.append((variant, start, end))
		
		variants3 = []
		for variant, start, end in variants2:
			if optional_match := OPTIONAL_LETTERS.fullmatch(variant):
				letter = optional_match['letter']
				variants3.append(
					(variant.replace(f'({letter})', letter), start, end)
				)
				variants3.append(
					(variant.replace(f'({letter})', ''), start, end)
				)
			else:
				variants3.append((variant, start, end))

		variants4 = []
		for variant, start, end in variants3:
			alt_affix = None
			if variant.startswith('-'):
				alt_affix = variant[1:]
			elif variant.endswith('-'):
				alt_affix = variant[:-1]
			if alt_affix:
				try:
					variant = re.sub(ALT_SUFFIX_FORMS[variant], alt_affix, self.headword_form)
				except Exception:
					pass
			variants4.append((variant, start, end))

		return variants4

	def _drop_invalid_forms(self, variants):
		new_variants = []
		for variant, start, end in variants:
			if variant in self.manual_exclusions:
				continue
			if not WORD_REGEX.fullmatch(variant):
				continue
			if self.variant_rejector and self.variant_rejector.fullmatch(variant):
				continue
			new_variants.append((variant, start, end))
		return new_variants

	def _resolve_cross_references(self, cross_refs):
		'''
		If an entry makes reference to a common affix (e.g. -ness, -ity), we
		add in the possible spellings of those affixes.
		'''
		cross_ref_ids = []
		for cross_ref in cross_refs:
			try:
				cross_ref_id = OED_URL_PARSER.search(cross_ref['href'])['lemma_id']
			except:
				continue
			if cross_ref_id != self.lemma_id:
				cross_ref_ids.append(cross_ref_id)
		lemma_refs = [cross_ref for cross_ref in cross_ref_ids if cross_ref.endswith(('_n', '_v', '_adj', '_n1', '_v1', '_adj1'))]
		affix_refs = [cross_ref for cross_ref in cross_ref_ids if cross_ref.endswith(('_suffix', '_suffix1', '_prefix', '_prefix1'))]
		
		if len(lemma_refs) == 1 and len(affix_refs) == 1:
			lemma_ref = lemma_refs[0]
			affix_ref = affix_refs[0]
			if affix_ref not in OED_AFFIXES:
				return
			if lemma_match := OED_LEMMA_MAPPER.search(lemma_ref):
				sub_lemma_id = lemma_match["id"]
				if (OED_CACHE_DIR / f'{sub_lemma_id}.html').exists():
					subparser = OEDLemmaParser(sub_lemma_id, do_not_resolve_cross_references=True)
					subparser.access()
					subparser.parse()
					head_variants = subparser._temp_variants
			
					affix, affix_type = affix_ref.split('_')
					if affix_type.endswith('1'):
						affix_type = affix_type[:-1]
					if affix_type == 'prefix':
						search_string = f'^{affix}'
					else:
						search_string = f'{affix}$'
					for head_variant, h_start, h_end in head_variants:
						for alternate_affix, a_start, a_end in OED_AFFIXES[affix_ref]:
							if h_start < a_start or h_end > a_end:
								continue
							if affix_type == 'prefix':
								variant = alternate_affix + head_variant
							else:
								variant = head_variant + alternate_affix
							self._temp_variants.append((variant, h_start, h_end))
		
		elif len(lemma_refs) == 0 and len(affix_refs) == 1:
			affix_ref = affix_refs[0]
			if affix_ref not in OED_AFFIXES:
				return
			affix, affix_type = affix_ref.split('_')
			if affix_type.endswith('1'):
				affix_type = affix_type[:-1]
			if affix_type == 'prefix':
				search_string = f'^{affix}'
			else:
				search_string = f'{affix}$'
			for alternate_affix, start, end in OED_AFFIXES[affix_ref]:
				variant = re.sub(search_string, alternate_affix, self.headword_form)
				self._temp_variants.append((variant, start, end))

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

	####################
	# EXTRACT QUOTATIONS
	####################

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
			if year := self._normalize_date_to_year(date.text):
				if quote := self._extract_quotation(body):
					if keyword := self._extract_keyword(body):
						quotes.add((year, keyword, quote))
		return list(quotes)

	#############################
	# MAP VARIANTS AND QUOTATIONS
	#############################

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

	def _create_mapping(self, drop_unattested_variants):
		'''
		Map each extracted quote onto an extracted variant.
		'''
		variant_quote_map = {variant: [] for variant, s, e, v in self.variants}
		for year, keyword, quote in self.quotations:
			if variant := self._map_quote_to_variant(year, keyword, quote):
				variant_quote_map[variant].append((year, quote))
		if drop_unattested_variants:
			variant_quote_map = {variant: quotes for variant, quotes in variant_quote_map.items() if len(quotes) > 0}
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
		except Exception:
			print(f'- Failed to access {lemma}; continuing...')

		try:
			oed_lemma_parser.parse()
		except Exception:
			print(f'- Failed to parse {lemma}; continuing...')
			continue

		if len(oed_lemma_parser.variants_to_quotations) > 0:
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
