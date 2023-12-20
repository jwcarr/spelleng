from time import sleep
from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup
from utils import json_read, json_write


HTTP_REQUEST_HEADERS = {
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15',
}

LEMMA_ID_PARSER = re.compile(r'/dictionary/(?P<lemma_id>.+?)\?')


def get_lemmata_for_word(word):
	url = f'https://www.oed.com/search/dictionary/?scope=Entries&q={word}'
	try:
		req = requests.get(url, headers=HTTP_REQUEST_HEADERS)
		results_page = BeautifulSoup(req.text, 'lxml')
		results_section = results_page.find('div', class_='simpleResultsLeft')
		result_titles = results_section.find_all('h3', class_='resultTitle')
		lemmata = []
		for title in result_titles:
			link = title.find('a')
			if match :=LEMMA_ID_PARSER.match(link['href']):
				lemmata.append(match['lemma_id'])
		return lemmata
	except Exception:
		print(f'- Parsing error for word: {word}')
		return []

def maps_words_to_lemmata(words_file, lemmata_file, start_from=0, delay=0):
	words = json_read(words_file)
	words = [word for word in words.keys()]
	lemmata_file = lemmata_file.with_suffix('.txt')
	for i, word in enumerate(words[start_from:], start_from):
		lemmata = get_lemmata_for_word(word)
		lemmata_str = ', '.join(lemmata)
		output_str = f'{word} : {lemmata_str}\n'
		with open(lemmata_file, 'a') as file:
			file.write(output_str)
		print(i, output_str.strip())
		sleep(delay)

def convert_temp_file_to_json(words_file, lemmata_file):
	word_to_lemmata = {}
	with open(lemmata_file.with_suffix('.txt')) as file:
		for line in file:
			if line:
				word, lemmata = line.split(' : ')
				lemmata = lemmata.strip()
				if lemmata == '':
					lemmata = []
				else:
					lemmata = lemmata.split(', ')
				word_to_lemmata[word] = lemmata
	json_write(word_to_lemmata, lemmata_file.with_suffix('.json'))


if __name__ == '__main__':

	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('words_file', action='store', type=str, help='file containing words to map to lemmata')
	parser.add_argument('lemmata_file', action='store', type=str, help='output lemmata file')
	parser.add_argument('--start', action='store', type=int, default=0, help='lemma number to start from')
	parser.add_argument('--delay', action='store', type=int, default=0, help='delay (in seconds) between each lemma extraction/parsing')
	args = parser.parse_args()

	words_file = Path(args.words_file)
	lemmata_file = Path(args.lemmata_file)

	maps_words_to_lemmata(words_file, lemmata_file, args.start, args.delay)
	convert_temp_file_to_json(words_file, lemmata_file)
