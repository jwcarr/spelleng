from pathlib import Path
import re
from collections import defaultdict
from bs4 import BeautifulSoup
from utils import json_write, json_read


ROOT = Path(__file__).parent.parent.resolve()

WORD_REGEX = re.compile(r'[abcdefghijklmnopqrstuvwxyzæðþęłȝꝥ]+')


HELSINKI_BAND_MAPPING = {
	'O1': 'Old English (I)',
	'O2': 'Old English (II)',
	'O3': 'Old English (III)',
	'O4': 'Old English (IV)',
	'O1/2': 'Old English (II)',
	'O2/3': 'Old English (III)',
	'O2/4': 'Old English (IV)',
	'O3/4': 'Old English (IV)',
	'OX/2': 'Old English (II)',
	'OX/3': 'Old English (III)',
	'OX/4': 'Old English (IV)',
	'M1': 'Middle English (I)',
	'M2': 'Middle English (II)',
	'M3': 'Middle English (III)',
	'M4': 'Middle English (IV)',
	'M2/3': 'Middle English (III)',
	'M2/4': 'Middle English (IV)',
	'M3/4': 'Middle English (IV)',
	'MX/1': 'Middle English (I)',
	'MX/2': 'Middle English (II)',
	'MX/4': 'Middle English (IV)',
	'E1': 'Early Modern English (I)',
	'E2': 'Early Modern English (II)',
	'E3': 'Early Modern English (III)',
}

CLMET_BAND_MAPPING = {
	"1710-1780": "Late Modern English (I)",
	"1780-1850": "Late Modern English (II)",
	"1850-1920": "Late Modern English (III)",
}


def normalize_text(text):
	'''
	Convert a text to lowercase and strip all non-alphabetical characters.
	'''
	return re.sub(r'[^\w\s]', '', text.strip().lower())


def parse_helsinki(corpus, input_xml):
	with open(input_xml) as file:
		soup = BeautifulSoup(file, 'xml')
	for tag in soup.find_all('foreign'):
		tag.decompose()
	for tag in soup.find_all('note'):
		tag.decompose()
	for document in soup.teiCorpus.find_all('TEI'):
		head = document.find('teiHeader')
		text = document.find('text')
		author = head.fileDesc.titleStmt.author.get_text()
		title = head.fileDesc.titleStmt.title.get_text()
		date = head.profileDesc.creation.date.get_text()
		band = HELSINKI_BAND_MAPPING[document['n']]
		if band is None:
			print(date)
			continue
		tokens = []
		for line in text.get_text().split('\n'):
			if line := line.strip():
				for word in normalize_text(line).split(' '):
					if WORD_REGEX.fullmatch(word.strip()):
						tokens.append(word + '_')
		corpus[band].append(
			{
				'author': author,
				'title': title,
				'date': date,
				'text': ' '.join(tokens),
			}
		)


def parse_clmet(corpus, input_dir):
	for text_file in input_dir.iterdir():
		print(text_file)
		with open(text_file) as file:
			soup = BeautifulSoup(file, 'lxml')
		author = soup.find('author').text
		title = soup.find('title').text
		date = soup.find('year').text
		period = soup.find('period').text
		band = CLMET_BAND_MAPPING[period]
		tokens = []
		text = soup.find('text')
		for paragraph in text.find_all('p'):
			for token in normalize_text(paragraph.text.replace('\n', ' ')).split(' '):
				if token:
					word, pos = token.split('_')
					if WORD_REGEX.fullmatch(word.strip()):
						tokens.append(token)
		corpus[band].append(
			{
				'author': author,
				'title': title,
				'date': date,
				'text': ' '.join(tokens),
			}
		)


def count_corpus(corpus):
	counts_by_band = {}
	for band, documents in corpus.items():
		word_counts = defaultdict(int)
		for document in documents:
			for token in document['text'].split(' '):
				word, pos = token.split('_')
				word_counts[word] += 1
		print(band, f'{len(documents):,}', f'{sum(word_counts.values()):,}', f'{len(word_counts):,}')


if __name__ == '__main__':

	corpus = {
		"Old English (I)": [],
		"Old English (II)": [],
		"Old English (III)": [],
		"Old English (IV)": [],
		"Middle English (I)": [],
		"Middle English (II)": [],
		"Middle English (III)": [],
		"Middle English (IV)": [],
		"Early Modern English (I)": [],
		"Early Modern English (II)": [],
		"Early Modern English (III)": [],
		"Late Modern English (I)": [],
		"Late Modern English (II)": [],
		"Late Modern English (III)": [],
	}

	parse_helsinki(
		corpus,
		ROOT / 'data' / 'helsinki' / 'HC_XML_Master_v9f.xml',
	)

	parse_clmet(
		corpus,
		ROOT / 'data' / 'clmet' / 'corpus' / 'txt' / 'pos',
	)

	for band, documents in corpus.items():
		documents.sort(key=lambda d: d['date'])

	json_write(
		corpus,
		ROOT / 'data' / 'corpus.json'
	)

	count_corpus(corpus)
