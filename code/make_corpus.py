from pathlib import Path
import re
from collections import defaultdict
from bs4 import BeautifulSoup
from utils import json_write, json_read


ROOT = Path(__file__).parent.parent.resolve()

WORD_REGEX = re.compile(r'[abcdefghijklmnopqrstuvwxyzæðþęłȝꝥ]+')
YEAR_REGEX = re.compile(r'(?P<year>\d{4})')


HELSINKI_BAND_MAPPING = {
	'O1': ('Old English (I & II)', 900),
	'O2': ('Old English (I & II)', 900),
	'O3': ('Old English (III)', 1000),
	'O4': ('Old English (IV)', 1100),
	'O1/2': ('Old English (I & II)', 900),
	'O2/3': ('Old English (III)', 1000),
	'O2/4': ('Old English (IV)', 1100),
	'O3/4': ('Old English (IV)', 1100),
	'OX/2': ('Old English (I & II)', 900),
	'OX/3': ('Old English (III)', 1000),
	'OX/4': ('Old English (IV)', 1100),
	'M1': ('Middle English (I)', 1200),
	'M2': ('Middle English (II)', 1300),
	'M3': ('Middle English (III)', 1400),
	'M4': ('Middle English (IV)', 1450),
	'M2/3': ('Middle English (III)', 1400),
	'M2/4': ('Middle English (IV)', 1450),
	'M3/4': ('Middle English (IV)', 1450),
	'MX/1': ('Middle English (I)', 1200),
	'MX/2': ('Middle English (II)', 1300),
	'MX/4': ('Middle English (IV)', 1450),
	'E1': ('Early Modern English (I)', 1550),
	'E2': ('Early Modern English (II)', 1600),
	'E3': ('Early Modern English (III)', 1650),
}

CLMET_BAND_MAPPING = {
	"1710-1780": "Late Modern English (I)",
	"1780-1850": "Late Modern English (II)",
	"1850-1920": "Late Modern English (III)",
}

HELSINKI_LETTER_DATES = {
	("Alice Hatton", "Letters (to her father)"): 1699,
	("Anne Hatton", "Letters (to her father)"): 1695,
	("Anonymous", "A Letter by the Commissioner of Customs (to Lord Clifford)"): 1672,
	("Anonymous", "A Letter by the Fellow of Trinity College (to Lord Burghley)"): 1594,
	("Anonymous", "A Letter by the Privy Council (to Lord Rochester)"): 1688,
	("Arthur Capel", "Letters (to the King)"): 1677,
	("Brilliana Harley", "Letters (to her husband)"): 1625,
	("Charles Hatton", "Letter (to his wife)"): 1690,
	("Charles II", "Letters (to Lord Essex)"): 1674,
	("Edward Conway", "Letter (to Lord Buckingham)"): 1623,
	("Elizabeth Hatton", "Letter (to her son)"): 1666,
	("Elizabeth I", "Letter (to Sir Thomas Edmondes)"): 1598,
	("Elizabeth Masham", "Letters (to her mother)"): 1629,
	("Elizabeth Oxinden", "Letters (to her mother-in-law)"): 1665,
	("Frances Hatton", "Letter (to her husband)"): 1677,
	("Francis Aungier", "Letter (to Lord Essex)"): 1675,
	("Henry Oxinden", "Letters (to his wife)"): 1662,
	("Jane Pinney", "Letter (to her daughter)"): 1685,
	("Joan Everard", "Letters (to her mother)"): 1628,
	("John Barrington", "Letters (to his mother)"): 1629,
	("John Pinney", "Letter (to his daughter)"): 1688,
	("John Somers", "Letter (to the King)"): 1697,
	("John Strype", "Letters (to his mother)"): 1664,
	("Katherine Oxinden", "Letter (to her son)"): 1634,
	("Katherine Paston", "Letters (to her son)"): 1624,
	("Mary Peyton", "Letter (to her daughter)"): 1632,
	("Mary Proud", "Letter (to her mother)"): 1626,
	("Nicholas Haddock", "Letter (to his father)"): 1706,
	("Philip Gawdy", "Letter (to his father)"): 1587,
	("Philip Henry", "Letter (to his wife)"): 1685,
	("Richard Haddock Jr", "Letter (to his father)"): 1692,
	("Richard Haddock Sr", "Letters (to his wife)"): 1672,
	("Richard Oxinden", "Letters (to his son)"): 1626,
	("Robert Cecil", "Letters (to Sir Thomas Edmondes)"): 1597,
	("Robert Spencer", "Letters (to the King's agent)"): 1687,
	("Thomas Barrington", "Letter (to his mother)"): 1629,
	("Thomas Edmondes", "Letter (to Sir Robert Cecil)"): 1598,
	("Thomas Knyvett", "Letters (to his wife)"): 1620,
	("Thomas Osborne", "Letters (to Lord Essex)"): 1675,
	("Valentine Pettit", "Letters (to her son)"): 1624,
	("William Cecil", "Letter (to the University of Cambridge)"): 1588,
	("William Paston", "Letters (to his mother)"): 1624,
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
		band, year = HELSINKI_BAND_MAPPING[document['n']]
		if (author, title) in HELSINKI_LETTER_DATES:
			year = HELSINKI_LETTER_DATES[(author, title)]
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
				'year': year,
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
		year = int(YEAR_REGEX.search(soup.find('year').text)['year'])
		if year == 1920:
			continue # only take texts upto and including 1919
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
				'year': year,
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
		"Old English (I & II)": [],
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
		documents.sort(key=lambda d: d['year'])

	json_write(
		corpus,
		ROOT / 'data' / 'corpus.json'
	)

	count_corpus(corpus)
