from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup
from utils import json_read, json_write


ROOT = Path(__file__).parent.parent.resolve()

HTTP_REQUEST_HEADERS = {
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15',
}

LEMMA_ID_PARSER = re.compile(r'/dictionary/(?P<lem>[abcdefghijklmnopqrstuvwxyzæðþęłȝꝥ]+?)_(?P<pos>adj|n|v)(?P<num>\d?)\?')

CLMET_POS_REWRITES = {'nn': 'n', 'vb': 'v', 'jj': 'adj'}

PERIOD_MAP = {
	'Old English': {'start': 800, 'end': 1150},
	'Middle English': {'start': 1150, 'end': 1500},
	'1500s': {'start': 1500, 'end': 1600},
	'1600s': {'start': 1600, 'end': 1700},
	'1700s': {'start': 1700, 'end': 1800},
	'1800s': {'start': 1800, 'end': 1900},
	'1900s': {'start': 1900, 'end': 2000},
	'2000s': {'start': 2000, 'end': 2100},
}


def create_token_map(corpus):
	token_map = {band: {} for band in corpus}
	for band, documents in corpus.items():
		for doc_i, document in enumerate(documents):
			for token in document['text'].split(' '):
				if token in token_map[band]:
					token_map[band][token][0].add(doc_i)
					token_map[band][token][1] += 1
				else:
					token_map[band][token] = [{doc_i}, 1, None]
		for token, token_data in token_map[band].items():
			token_data[0] = len(token_data[0])
	return token_map

def parse_period(text_period):
	start_text, end_text = text_period.split('–')
	if start_text.startswith(('a', 'c')):
		start_text = start_text[1:]
	if end_text.startswith(('a', 'c')):
		end_text = end_text[1:]
	try:
		start = int(start_text)
	except ValueError:
		start = PERIOD_MAP[start_text]['start']
	try:
		end = int(end_text)
	except ValueError:
		if end_text == '':
			end = 2100
		else:
			end = PERIOD_MAP[end_text]['end']
	return start, end

def get_lemma_for_token(token, target_year, target_pos=None):
	url = f'https://www.oed.com/search/dictionary/?scope=Entries&q={token}'
	req = requests.get(url, headers=HTTP_REQUEST_HEADERS)
	results_page = BeautifulSoup(req.text, 'lxml')
	result_divs = results_page.find_all('div', class_='resultsSetItem')
	for result_div in result_divs:
		usage_period = result_div.find('span', class_='dateRange').text
		entry_link = result_div.find('a', class_='viewEntry')['href']
		if match := LEMMA_ID_PARSER.match(entry_link):
			if target_pos is None or target_pos == match['pos']:
				start, end = parse_period(usage_period)
				if target_year >= start and target_year <= end:
					return f"{match['lem']}_{match['pos']}{match['num']}"
	return None

def get_unique_forms(token_map):
	unique_forms = []
	for band, tokens in token_map.items():
		# if not band.startswith('Late'):
		# 	continue
		for token, data in tokens.items():
			if data[0] < 2:
				continue
			wordform, pos = token.split('_')
			if len(wordform) < 3:
				continue
			if pos == '' or pos in ('nn', 'jj', 'vb'):
				unique_forms.append(wordform)
	return sorted(list(set(unique_forms)))


{'search_term': 'minum', 'results':[ ['minnow_n', 1425, 2100],  ]}


if __name__ == '__main__':

	# corpus = json_read(ROOT / 'data' / 'corpus.json')
	# token_map = create_token_map(corpus)
	# json_write(token_map, ROOT / 'data' / 'token_map.json')

	token_map = json_read(ROOT / 'data' / 'token_map.json')
	print(len(get_unique_forms(token_map)))

	# print(get_lemma_for_token('minum', 900, None))
