from pathlib import Path
import json


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'
OED = DATA / 'oed_quotations'


EXPECTED_COUNTS = {
	'man_n': {'mahn': 0, 'man': 600, 'mane': 2, 'mann': 7, 'manna': 2, 'manne': 3, 'maun': 0, 'min': 2, 'mon': 17, 'mone': 0, 'monn': 0, 'monna': 0, 'monne': 1, 'mun': 5},
	'crumple_v': {'cromple': 0, 'crompull': 1, 'crompyl': 0, 'crumple': 10},
	'underhand_adj': {'underhand': 17},
	'angle_v': {'angle': 6},
	'angle_n': {'ancgel': 0, 'ancgil': 0, 'angel': 2, 'angell': 0, 'angil': 0, 'angle': 15, 'angul': 0, 'angylle': 1, 'hangle': 0, 'hangul': 0, 'ongel': 0, 'ongul': 1},
	'life_n': {'hlif': 0, 'layf': 0, 'layffe': 0, 'lef': 0, 'lefe': 0, 'leif': 0, 'leife': 0, 'leive': 0, 'leue': 1, 'leyf': 0, 'lief': 5, 'liefe': 0, 'lieff': 0, 'lieiw': 0, 'lieve': 0, 'lif': 40, 'life': 687, 'liff': 2, 'liffe': 1, 'liif': 1, 'lijf': 7, 'lijfe': 0, 'liue': 18, 'liuf': 0, 'live': 0, 'liyf': 0, 'liyffe': 0, 'lyef': 0, 'lyefe': 0, 'lyeff': 0, 'lyf': 20, 'lyfe': 23, 'lyff': 4, 'lyffe': 3, 'lyfve': 0, 'lyif': 0, 'lyife': 0, 'lyiff': 0, 'lyue': 9, 'lyve': 0, 'lywe': 0, 'lyyf': 0},
	'mind_n': {'maind': 0, 'maynd': 0, 'maynde': 0, 'meand': 0, 'meend': 0, 'meende': 1, 'meinde': 0, 'mend': 2, 'mende': 10, 'meynd': 0, 'meynde': 0, 'miend': 0, 'miende': 0, 'min': 2, 'mind': 435, 'minde': 48, 'mine': 0, 'muinde': 0, 'mund': 1, 'munde': 6, 'muynde': 6, 'myend': 1, 'myende': 1, 'myn': 0, 'mynd': 33, 'myndd': 0, 'myndde': 0, 'mynde': 133, 'myne': 1, 'myynde': 0},
	
}


def json_read(input_file):
	with open(input_file) as file:
		data = json.load(file)
	return data


def test_man_n():
	for lemma, variant_counts in EXPECTED_COUNTS.items():
		lemma_data = json_read(OED / f'{lemma}.json')
		for variant, quotations in lemma_data.items():
			assert len(quotations) == variant_counts[variant]


if __name__ == '__main__':

	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('lemma', action='store', type=str, help='lemma to count')
	args = parser.parse_args()

	expected_counts = {}
	lemma_data = json_read(OED / f'{args.lemma}.json')
	for variant, quotations in lemma_data.items():
		expected_counts[variant] = len(quotations)
	print(expected_counts)
