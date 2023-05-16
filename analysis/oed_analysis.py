from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup, NavigableString
from utils import json_read


ROOT = Path(__file__).parent.parent.resolve()

DATE_REGEX = re.compile(r'^((e|l)?OE)|^((c|a)?\d{3,4})')
ENTRY_REGEX = re.compile(r'Entry/(\d+)\?')
WORD_REGEX = re.compile(r'[abcdefghijklmnopqrstuvwxyzæðþęłȝꝥ]+')

HEADERS = {
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15',
}


def remove_whitespace(text):
	return ' '.join([line.replace('\xa0', ' ').strip() for line in text.split('\n')])

def date_quotation(citation):
	if date_extract := DATE_REGEX.match(citation):
		if date_extract[0] == 'eOE':
			return 800
		if date_extract[0] == 'OE':
			return 900
		if date_extract[0] == 'lOE':
			return 1000
		if date_extract[0].startswith('c'):
			return int(date_extract[0][1:])
		if date_extract[0].startswith('a'):
			return int(date_extract[0][1:])
		return int(date_extract[0])
	return False

def save_oed_page(url):
	if entry_id := ENTRY_REGEX.search(url):
		entry_path = ROOT / 'data' / 'oed' / f'{entry_id[1]}.html'
		if entry_path.exists():
			return entry_id[1]
		req = requests.get(url, headers=HEADERS)
		with open(entry_path, 'w') as file:
			file.write(req.text)
		return entry_id[1]
	raise ValueError('Invalid URL: Could not parse entry ID')

def parse_forms(entry_id):
	with open(ROOT / 'data' / 'oed' / f'{entry_id}.html') as file:
		soup = BeautifulSoup(file, 'lxml')
	forms = set()
	forms_div = str(soup.find('div', class_='forms'))
	if 'Plural.' in forms_div:
		forms_div = forms_div.split('Plural.')[0]
	for form_info in forms_div.split(','):
		s = BeautifulSoup(form_info, 'lxml')
		if 'error' in s.text:
			continue # ignore (possible) transmission errors
		if strong_form := s.find('strong'):
			if form := WORD_REGEX.match(strong_form.text):
				forms.add(form[0])
	return list(forms)

def parse_quotes(entry_id, forms):
	with open(ROOT / 'data' / 'oed' / f'{entry_id}.html') as file:
		soup = BeautifulSoup(file, 'lxml')
	finds = []
	for quote in soup.find_all("div", class_="quotation"):
		try:
			cite = remove_whitespace(quote.find('span', class_='noIndent').text)
			form = remove_whitespace(quote.find('span', class_='quotationKeyword').text)
		except:
			continue
		if form in forms:
			if date := date_quotation(cite):
				finds.append((form, date))
	return finds

def put_into_bands(finds, n_bands=12):
	band_width = (2000 - 800) // n_bands
	bands = {}
	for start in range(800, 2000, band_width):
		end = start + band_width - 1
		bands[(start, end)] = set()
	for form, date in finds:
		for start, end in bands:
			if date >= start and date <= end:
				bands[start, end].add(form)
				break
	return bands





if __name__ == '__main__':

	url = 'https://www.oed.com/view/Entry/86918?rskey=DfoOHz&result=1&isAdvanced=false#eid'
	entry_id = save_oed_page(url)

	forms = parse_forms(entry_id)
	finds = parse_quotes(entry_id, forms)

	banded = put_into_bands(finds, 12)
	for period, forms in banded.items():
		print(period)
		print(forms)

	# hc_word_counts = json_read(ROOT / 'data' / 'hc_word_counts.json')


	# for form in forms:
	# 	count = hc_word_counts.get(form, 0)
	# 	print(str(count).zfill(3), form)





