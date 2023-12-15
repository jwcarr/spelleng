
	def classify_band(self, date):
		for (start, end), band in BROAD_BANDS.items():
			if date >= start and date < end:
				return band
		return None

	def classify(self):
		data = {band: {f: 0 for f, s, e in self.variants} for period, band in BROAD_BANDS.items()}
		for variant, quotes in self.quotes.items():
			for date, quote in quotes:
				band = self.classify_band(date)
				if band:
					data[band][variant] += 1
		return data





if __name__ == '__main__':

	page = '''<!DOCTYPE HTML>
<html lang='en'>
<head>
<meta charset='utf-8' />
<title>OED Analysis</title>
</head>
<body>'''

	lexemes = ['man_n1', 'god_n', 'duke_n', 'king_n', 'lord_n', 'father_n', 'place_n1', 'brother_n', 'world_n', 'house_n1', 'child_n', 'woman_n', 'body_n', 'water_n', 'time_n', 'work_n', 'folk_n', 'word_n', 'grace_n', 'name_n', 'bishop_n', 'wife_n', 'life_n', 'son_n1', 'earth_n1', 'daughter_n', 'matter_n1', 'lady_n', 'master_n1', 'hand_n', 'knight_n', 'love_n1', 'church_n1', 'night_n', 'heart_n', 'mercy_n', 'power_n1']


	# lexemes = ['life_n']


	lemma_map = json_read('../data/lemma_map.json')

	periods = []
	
	for lexeme in lexemes[:]:

		print(lexeme)

		page += f'<h2>{lexeme}</h2>'

		table = '<table>\n'

		headword = lexeme.split('_')[0]
		hel_data = lemma_map[headword]

		lemma = OEDLemma(lexeme)
		oed_data = lemma.classify()

		periods.extend(lemma.periods)

		for period in ['Old English', 'Middle English', 'Early Modern English']:

			table += f'<tr><td colspan=3 style="line-height: 40px"><i>{period}</i></td></tr>\n'

			combined_forms = sorted(list(set(list(hel_data[period].keys()) + list(oed_data[period].keys()))))
			for form in combined_forms:
				try:
					hel_c = hel_data[period].get(form, '')
				except KeyError:
					hel_c = ''
				try:
					oed_c = oed_data[period].get(form, '✘')
				except KeyError:
					oed_c = ''

				table += f'<tr><td>{form}</td><td>{hel_c}</td><td>{oed_c}</td></tr>\n'


		table += '</table>\n'
		page += table

		page += '''
		</body>
		</html>
		'''

		print('------------------------------------')

	with open('/Users/jon/Desktop/output.html', 'w') as file:
		file.write(page)

	with open('../data/periods.json', 'w') as file:
		file.write(str(set(periods)))
