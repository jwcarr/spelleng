from pathlib import Path
import pandas as pd
from utils import json_write


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'


morpholex_pos_to_oed_pos = {}


morpholex_data_path = DATA / 'MorphoLEX_en.xlsx'

sheet_names = ['0-1-0', '0-1-1', '0-1-2', '0-1-3', '0-1-4', '0-2-0', '0-2-1', '0-2-2', '0-2-3', '0-3-0', '0-3-1', '0-3-2', '0-4-0', '1-1-0', '1-1-1', '1-1-2', '1-1-3', '1-1-4', '1-2-0', '1-2-1', '1-2-2', '1-2-3', '1-3-0', '2-1-0', '2-1-1', '2-1-2', '2-1-3', '2-2-0', '3-1-0', '0-0-0']

morpholex_dataframes = pd.read_excel(morpholex_data_path, sheet_name=sheet_names, keep_default_na=False)
dataframes_to_concatenate = []
for pattern, dataframe in morpholex_dataframes.items():
	dataframe.drop(
		labels=dataframe.columns.difference(['Word', 'POS', 'MorphoLexSegm']),
		axis='columns',
		inplace=True,
	)
	dataframes_to_concatenate.append(dataframe)
merged_dataframe = pd.concat(dataframes_to_concatenate, ignore_index=True)

morpholex_word_errors = {
	"(altern)>ate>": "alternate",
	"(altern)>ate>d": "alternate",
	"(altern)>ate>ly": "alternately>",
	"(altern)>ate>s": "alternate",
	"(anim)>ose>>ity>": "animosity",
	"<inter<(medi)>ory>": "intermediary",
}

words = {}
for index, row in merged_dataframe.iterrows():
	word = row['Word']
	if not isinstance(word, str):
		word = str(word).lower()
	if word in morpholex_word_errors:
		word = morpholex_word_errors[word]
	for pos in row["POS"].split('|'):
		word_id = f'{word}_{pos}'
		words[word_id] = row['MorphoLexSegm']

words = {k: words[k] for k in sorted(list(words.keys()))}

json_write(words, DATA / DATA / 'morpholex.json')
