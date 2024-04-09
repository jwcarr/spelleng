from pathlib import Path
import json


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'
OED = DATA / 'oed_quotations_v1'


EXPECTED_COUNTS = {
	'man_n': {'mahn': 0, 'man': 600, 'mane': 2, 'mann': 7, 'manna': 2, 'manne': 3, 'maun': 0, 'min': 2, 'mon': 17, 'mone': 0, 'monn': 0, 'monna': 0, 'monne': 1, 'mun': 5},
	'crumple_v': {'cromple': 0, 'crompull': 1, 'crompyl': 0, 'crumple': 10},
	'underhand_adj': {'underhand': 17},
	'angle_v': {'angle': 6},
	'angle_n': {'ancgel': 0, 'ancgil': 0, 'angel': 2, 'angell': 0, 'angil': 0, 'angle': 15, 'angul': 0, 'angylle': 1, 'hangle': 0, 'hangul': 0, 'ongel': 0, 'ongul': 1},
	'life_n': {'hlif': 0, 'layf': 0, 'layffe': 0, 'lef': 0, 'lefe': 0, 'leif': 0, 'leife': 0, 'leive': 0, 'leue': 1, 'leyf': 0, 'lief': 5, 'liefe': 0, 'lieff': 0, 'lieiw': 0, 'lieve': 0, 'lif': 41, 'life': 687, 'liff': 2, 'liffe': 1, 'liif': 1, 'lijf': 7, 'lijfe': 0, 'liue': 18, 'liuf': 0, 'live': 0, 'liyf': 0, 'liyffe': 0, 'lyef': 0, 'lyefe': 0, 'lyeff': 0, 'lyf': 20, 'lyfe': 23, 'lyff': 4, 'lyffe': 3, 'lyfve': 0, 'lyif': 0, 'lyife': 0, 'lyiff': 0, 'lyue': 9, 'lyve': 0, 'lywe': 0, 'lyyf': 0},
	'mind_n': {'maind': 0, 'maynd': 0, 'maynde': 0, 'meand': 0, 'meend': 0, 'meende': 1, 'meinde': 0, 'mend': 2, 'mende': 10, 'meynd': 0, 'meynde': 0, 'miend': 0, 'miende': 0, 'min': 2, 'mind': 434, 'minde': 48, 'mine': 0, 'muinde': 0, 'mund': 1, 'munde': 6, 'muynde': 6, 'myend': 1, 'myende': 1, 'myn': 0, 'mynd': 33, 'myndd': 0, 'myndde': 0, 'mynde': 133, 'myne': 1, 'myynde': 0},
	
	# ROUND 1
	'moment_n': {'malmond': 0, 'mament': 0, 'mamonde': 0, 'mamont': 0, 'mamunt': 1, 'moment': 183, 'momente': 5, 'momentt': 0},
	'soul_n': {'saal': 1, 'sal': 1, 'sale': 0, 'sall': 2, 'salle': 1, 'saoul': 1, 'sauel': 1, 'sauele': 0, 'sauell': 0, 'sauil': 0, 'sauill': 0, 'saul': 10, 'saule': 17, 'saulen': 3, 'saull': 5, 'saulle': 0, 'sauul': 0, 'sauwel': 0, 'sauwil': 0, 'sauwl': 0, 'savl': 0, 'savle': 0, 'savll': 0, 'sawal': 0, 'sawel': 0, 'sawele': 0, 'sawell': 0, 'sawil': 1, 'sawill': 0, 'sawl': 3, 'sawle': 22, 'sawll': 1, 'sawlle': 0, 'sawol': 1, 'sawul': 1, 'sawule': 0, 'sawyl': 0, 'seawl': 0, 'seole': 0, 'shoul': 2, 'showl': 0, 'soal': 1, 'soale': 0, 'soawle': 0, 'sol': 0, 'sole': 2, 'soll': 0, 'solle': 0, 'sooal': 0, 'sool': 0, 'soole': 0, 'sooll': 0, 'souel': 0, 'souell': 0, 'soul': 282, 'soule': 86, 'soull': 1, 'soulle': 0, 'souȝl': 0, 'souȝle': 0, 'sovle': 0, 'sowal': 0, 'sowel': 0, 'sowele': 0, 'sowell': 0, 'sowile': 0, 'sowl': 1, 'sowle': 13, 'sowll': 0, 'sowlle': 0, 'sowul': 0, 'sowyl': 0, 'sowyll': 1, 'sowylle': 0, 'soyle': 0, 'sæul': 0, 'sæule': 0, 'sæwl': 0, 'sæwle': 0, 'zaule': 2, 'zawl': 0, 'zoal': 0, 'zoule': 0},
	'religion_n': {'ralegioun': 0, 'releegion': 0, 'relegeon': 0, 'relegion': 0, 'relegioun': 0, 'relegioune': 1, 'relegyon': 1, 'releidgeon': 0, 'reliegieoun': 1, 'religeon': 0, 'religeoun': 0, 'religeowne': 0, 'religion': 134, 'religione': 0, 'religioun': 12, 'religioune': 2, 'religiun': 9, 'religiune': 0, 'religon': 0, 'religyon': 3, 'religyone': 0, 'religyowne': 0, 'relligion': 0, 'relygeoun': 0, 'relygion': 2, 'relygione': 1, 'relygioun': 2, 'relygyon': 3, 'relygyone': 0, 'relygyoun': 0, 'relygyoune': 0, 'relygyown': 0, 'relygyowne': 0, 'relygyun': 0, 'riligioun': 0},
	'taste_n': {'taast': 4, 'taist': 2, 'tast': 26, 'taste': 60, 'test': 0},
	'lordship_n': {'hlaforscipe': 0, 'lauerdscape': 0, 'lauerscip': 0, 'lauerscipe': 0, 'lorchepe': 0, 'lorchipe': 1, 'lorchipp': 0, 'lorchuppe': 1, 'lordesship': 0, 'lordesshipp': 0, 'lordship': 31, 'lordyschype': 0, 'lorschip': 0, 'lorschipe': 0, 'lorshuppe': 0, 'lorshyp': 0, 'lortschyp': 0},
	'explain_v': {'explain': 63, 'explaine': 4, 'explane': 6, 'explayn': 0, 'explayne': 3},
	'prison_n': {'preason': 0, 'preasone': 0, 'preasoun': 0, 'preassoun': 0, 'preison': 0, 'preisone': 0, 'preisoun': 0, 'preissone': 0, 'preissonne': 0, 'preissoun': 0, 'presen': 0, 'presin': 0, 'preson': 1, 'presone': 0, 'presonn': 0, 'presonne': 0, 'presoun': 0, 'presoune': 0, 'presown': 0, 'presowne': 0, 'presowun': 0, 'presoyn': 0, 'presson': 0, 'pressone': 0, 'pressoun': 0, 'pressoyn': 0, 'pressun': 0, 'presun': 0, 'presune': 0, 'preysone': 0, 'preysoun': 0, 'prieson': 0, 'prisen': 0, 'prision': 0, 'prison': 51, 'prisone': 3, 'prisonne': 0, 'prisoun': 7, 'prisoune': 1, 'prisown': 0, 'prission': 0, 'prissone': 0, 'prissoun': 0, 'prissoune': 0, 'prisun': 4, 'prisund': 0, 'prisune': 2, 'prizen': 0, 'pruson': 0, 'prwsoun': 0, 'pryson': 4, 'prysone': 0, 'prysonne': 0, 'prysoun': 1, 'prysoune': 0, 'prysown': 0, 'pryssoun': 0, 'pryssune': 0, 'prysun': 0, 'prysyn': 0},
	'probability_n': {'probabilite': 2, 'probabilitie': 4, 'probability': 32, 'probabilte': 1, 'proprability': 0, 'provibility': 0},
	'excuse_n': {'escuse': 1, 'excuse': 38},
	'princess_n': {'prences': 0, 'prencess': 0, 'prencis': 0, 'prenssis': 0, 'princeis': 0, 'princes': 6, 'princess': 60, 'princesse': 7, 'princis': 0, 'prinses': 0, 'prynces': 0, 'pryncesse': 3, 'pryncis': 0, 'pryncise': 0, 'prynsace': 1, 'pryyncesse': 0},
	'learning_n': {'larnin': 1, 'learning': 33, 'leirning': 0, 'leorning': 0, 'leornung': 0, 'lerning': 1, 'lernyng': 6, 'lernynge': 3, 'lernyngh': 0, 'lernynghe': 1},
	'amuse_v': {'ammuse': 1, 'ammuze': 0, 'amuse': 44, 'amuze': 1},
	'sanction_n': {'sanction': 58},
	'improper_adj': {'improper': 21},
	'horn_n': {'heorn': 0, 'horn': 190, 'horne': 48, 'horun': 0},
	'serenity_n': {'serenity': 19},
	'clamour_n': {'clamor': 2, 'clamore': 1, 'clamour': 21, 'clamoure': 1, 'clamur': 1, 'clamure': 0},
	'benefit_v': {'benefit': 3, 'benefited': 4}, ### THIS NEEDS TO BE FIXED
	'construct_v': {'construct': 11},
	'incorrect_adj': {'incorrect': 11},
	'shorten_v': {'shorten': 31},
	'sole_n': {'soal': 2, 'soale': 3, 'soile': 1, 'soille': 0, 'sole': 88, 'sool': 0, 'soole': 2, 'soul': 0, 'soule': 2, 'sowle': 0},
	'loiter_v': {'leutere': 0, 'leutre': 0, 'lewtre': 0, 'loiter': 8, 'loitre': 0, 'loltre': 0, 'lotere': 0, 'lowtre': 0, 'loyeter': 0, 'loyter': 7, 'loytre': 0, 'loytron': 1},
	'lancet_n': {'lancet': 7, 'lancette': 0, 'launcet': 0, 'launcette': 1, 'lawncette': 0, 'lawnset': 0},
	'hydrant_n': {'hydrant': 3},

	
}


def json_read(input_file):
	with open(input_file) as file:
		data = json.load(file)
	return data


def test_man_n():
	for lemma, variant_counts in EXPECTED_COUNTS.items():
		lemma_data = json_read(OED / f'{lemma}.json')
		assert set(lemma_data.keys()) == set(variant_counts.keys())
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
