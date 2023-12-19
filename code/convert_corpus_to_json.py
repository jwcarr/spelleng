from pathlib import Path
from collections import defaultdict
from bs4 import BeautifulSoup
from utils import json_write


ROOT = Path(__file__).parent.parent.resolve()


DATE_TO_BROAD_BAND = {
	"–850": "Old English",
	"–1050": "Old English",
	"850–950": "Old English",
	"950–1050": "Old English",
	"1050–1150": "Old English",
	"1150–1500": "Middle English",
	"1150–1250": "Middle English",
	"1250–1350": "Middle English",
	"1350–1420": "Middle English",
	"1420–1500": "Middle English",
	"1500–1570": "Early Modern English",
	"1570–1640": "Early Modern English",
	"1640–1710": "Early Modern English",
}

DATE_TO_NARROW_BAND = {
	"–850": "Old English (I)",
	"–1050": None,
	"850–950": "Old English (II)",
	"950–1050": "Old English (III)",
	"1050–1150": "Old English (IV)",
	"1150–1500": None,
	"1150–1250": "Middle English (I)",
	"1250–1350": "Middle English (II)",
	"1350–1420": "Middle English (III)",
	"1420–1500": "Middle English (IV)",
	"1500–1570": "Early Modern English (I)",
	"1570–1640": "Early Modern English (II)",
	"1640–1710": "Early Modern English (III)",
}


def convert(input_xml, output_json, date_to_band_mapping):
	with open(input_xml) as file:
		soup = BeautifulSoup(file, 'xml')

	for tag in soup.find_all('foreign'):
		tag.decompose()
	for tag in soup.find_all('note'):
		tag.decompose()

	corpus = defaultdict(list)

	for document in soup.teiCorpus.find_all('TEI'):

		# extract header and text elements
		head = document.find('teiHeader')
		text = document.find('text')

		# extract relevant header info
		author = head.fileDesc.titleStmt.author.get_text()
		title = head.fileDesc.titleStmt.title.get_text()
		date = head.profileDesc.creation.date.get_text()

		band = date_to_band_mapping[date]
		if band is None:
			continue

		# clean up the text lines
		lines = []
		for line in text.get_text().split('\n'):
			if line := line.strip():
				lines.append(line)

		# store the document in the corpus
		corpus[band].append(
			{
				'author': author,
				'title': title,
				'date': date,
				'text': lines,
			}
		)

	json_write(corpus, output_json)


if __name__ == '__main__':

	convert(
		ROOT / 'data' / 'HC_XML_Master_v9f.xml',
		ROOT / 'data' / 'helsinki_corpus_broad.json',
		DATE_TO_BROAD_BAND,
	)

	convert(
		ROOT / 'data' / 'HC_XML_Master_v9f.xml',
		ROOT / 'data' / 'helsinki_corpus_narrow.json',
		DATE_TO_NARROW_BAND,
	)
