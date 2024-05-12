from collections import defaultdict
from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup
import utils


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'

HTTP_REQUEST_HEADERS = {
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15',
}

LEMMA_LINK_PARSER = re.compile(r'/dictionary/(?P<lemma_id>\w+_(?P<pos>[a-z]+)\d*)\?')
LEMMA_ID_PARSER = re.compile(r'(?P<wordform>\w+)_(?P<pos>[a-z]+)\d*')

CLMET_POS_REWRITES = {'nn': 'n', 'np': 'n', 'vb': 'v', 'jj': 'adj'}

PERIOD_MAP = {
	'Old English': {'start': 800, 'end': 1150},
	'late Old English': {'start': 1050, 'end': 1150},
	'Middle English': {'start': 1150, 'end': 1500},
	'1500s': {'start': 1500, 'end': 1600},
	'1600s': {'start': 1600, 'end': 1700},
	'1700s': {'start': 1700, 'end': 1800},
	'1800s': {'start': 1800, 'end': 1900},
	'1900s': {'start': 1900, 'end': 2000},
	'2000s': {'start': 2000, 'end': 2100},
}

STOP_WORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'may', 'must', 'shall']


def determine_lemma(oed_queries, token, year):
	'''
	Determine a token's lemma by selecting the first OED result that falls in
	the token's year and matches its pos.
	'''
	if oed_queries is None:
		return None
	wordform, pos = token.split('_')
	if wordform not in oed_queries:
		return None
	candidate_lemmata = oed_queries[wordform]['results']
	for lemma_id, lemma_pos, start, end in candidate_lemmata:
		if year >= start and year <= end:
			if pos == '' or CLMET_POS_REWRITES.get(pos[:2], None) == lemma_pos:
				return lemma_id
	return None


def count_corpus(corpus, oed_queries=None):
	'''
	Create a by-band count of all tokens in the corpus. For all unique forms,
	count the number of texts it occurs in (within band) and the number of
	tokens (within band). If oed_queries is provided, attempt to
	map each unique token to a lemma.
	'''
	corpus_counts = {band: {} for band in corpus}
	for band, documents in corpus.items():
		for doc_i, document in enumerate(documents):
			for token in document['text'].split(' '):
				if token in corpus_counts[band]:
					corpus_counts[band][token][0].add(doc_i)
					corpus_counts[band][token][1] += 1
				else:
					corpus_counts[band][token] = [
						{doc_i},
						1,
						determine_lemma(oed_queries, token, document['year'])
					]
		for token, token_data in corpus_counts[band].items():
			token_data[0] = len(token_data[0])
	return corpus_counts


def select_candidate_lemmata(corpus_counts):
	'''
	Select candidate lemmata from the corpus counts. We select all unique
	wordforms that occur in at least two texts within a given band and
	have a length of at least three characters. Additionally, we ignore
	Old English (since the OED doesn't have much coverage of OE and
	there's lots of problems with inflection), and, in the case of Late
	Modern, we only select uninflected forms.
	'''
	unique_forms = []
	for band, tokens in corpus_counts.items():
		if band.startswith('Old English'):
			continue # ignore Old English
		for token, (text_count, token_count, lemma_id) in tokens.items():
			if text_count == 1:
				continue # ignore tokens attested in only one text
			wordform, pos = token.split('_')
			if len(wordform) < 3:
				continue # ignore tokens shorter than three characters
			if pos == '' or pos in ('nn', 'jj', 'vb'):
				# ignore Late Modern tokens other than nouns, verbs, and
				# adjectives in their base forms
				unique_forms.append(wordform)
	return sorted(list(set(unique_forms)))


def parse_period(text_period):
	'''
	Parse an OED usage period into a start year and an end year.
	'''
	if text_period == '':
		return 800, 2100
	if text_period == 'Old English':
		return 800, 1150
	text_period = text_period.replace('?', '')
	text_period = text_period.replace('.', '0')
	if '–' not in text_period:
		text_period = f'{text_period}–{text_period}'
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
	return start - 10, end + 10


def perform_oed_search(token):
	'''
	Perform an OED search for the given token. The results page is parsed and
	the possible lemmata are returned with their POSs and usage periods.
	'''
	url = f'https://www.oed.com/search/dictionary/?scope=Entries&q={token}'
	req = requests.get(url, headers=HTTP_REQUEST_HEADERS)
	results_page = BeautifulSoup(req.text, 'lxml')
	result_divs = results_page.find_all('div', class_='resultsSetItem')
	results = []
	for result_div in result_divs:
		usage_period = result_div.find('span', class_='dateRange').text
		start, end = parse_period(usage_period)
		entry_link = result_div.find('a', class_='viewEntry')['href']
		if match := LEMMA_LINK_PARSER.match(entry_link):
			results.append((match['lemma_id'], match['pos'], start, end))
	return results


def search_candidate_tokens(candidate_tokens, results_file):
	'''
	Load the current state of the cache. Then search all tokens in the OED and
	add the reuslts to the cache. Returns the final state of the cache.
	'''
	if results_file.exists():
		cached_oed_queries = utils.json_read_lines(results_file, key='search_term')
	else:
		cached_oed_queries = {}
	for i, token in enumerate(candidate_tokens):
		if token in cached_oed_queries:
			continue
		print(i, token)
		query_results = {
			'search_term': token,
			'results': perform_oed_search(token)
		}
		utils.json_write_line(query_results, results_file)
	return utils.json_read_lines(results_file, key='search_term')


def extract_lemmata(token_map):
	'''
	Extract all noun, verb, and adjective lemmata from the corpus counts,
	excluding any stop words.
	'''
	lemmata = defaultdict(int)
	for band, tokens in token_map.items():
		for token, (text_count, token_count, lemma_id) in tokens.items():
			if lemma_id:
				parsed_lemma_id = LEMMA_ID_PARSER.match(lemma_id)
				if parsed_lemma_id['wordform'] in STOP_WORDS:
					continue
				if parsed_lemma_id['pos'] in ('n', 'v', 'adj'):
					lemmata[lemma_id] += token_count
	return {
		lemma_id: lemmata[lemma_id]
		for lemma_id in sorted(lemmata, key=lambda k: lemmata[k], reverse=True)
	}

if __name__ == '__main__':

	file_corpus = DATA / 'corpus.json'
	file_corpus_count = DATA / 'corpus_count.json'
	file_search_cache = DATA / 'oed_search_cache.json'
	file_lemmata = DATA / 'lemmata.json'

	# Extract tokens from the corpus and count tokens and texts
	corpus = utils.json_read(file_corpus)
	corpus_count = count_corpus(corpus)

	# Select candidate lemmata for searching in the OED
	candidate_tokens = select_candidate_lemmata(corpus_count)

	# Search candidate lemmata in the OED, caching the results along the way
	oed_queries = search_candidate_tokens(candidate_tokens, file_search_cache)

	# Perform the corpus count again, this time adding the lemmata using the OED queries
	corpus_count = count_corpus(corpus, oed_queries)
	utils.json_write(corpus_count, file_corpus_count)

	# Extract all lemmata and write out to JSON
	lemmata = extract_lemmata(corpus_count)
	utils.json_write(lemmata, file_lemmata)
