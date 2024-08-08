from pathlib import Path
import json


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'
OED_DATA = DATA / 'oed_data'


EXPECTED_COUNTS = {
	# ROUND 1
	'moment_n': {'malmond': 0, 'mament': 0, 'mamonde': 0, 'mamont': 0, 'mamunt': 1, 'moment': 183, 'momente': 5, 'momentt': 0},
	'soul_n': {'saal': 1, 'sal': 1, 'sale': 0, 'sall': 2, 'salle': 1, 'saoul': 1, 'sauel': 1, 'sauele': 0, 'sauell': 0, 'sauil': 0, 'sauill': 0, 'saul': 10, 'saule': 17, 'saulen': 3, 'saull': 5, 'saulle': 0, 'sauul': 0, 'sauwel': 0, 'sauwil': 0, 'sauwl': 0, 'savl': 0, 'savle': 0, 'savll': 0, 'sawal': 0, 'sawel': 0, 'sawele': 0, 'sawell': 0, 'sawil': 1, 'sawill': 0, 'sawl': 3, 'sawle': 22, 'sawll': 1, 'sawlle': 0, 'sawol': 1, 'sawul': 1, 'sawule': 0, 'sawyl': 0, 'seawl': 0, 'seole': 0, 'shoul': 2, 'showl': 0, 'soal': 1, 'soale': 0, 'soawle': 0, 'sol': 0, 'sole': 2, 'soll': 0, 'solle': 0, 'sooal': 0, 'sool': 0, 'soole': 0, 'sooll': 0, 'souel': 0, 'souell': 0, 'soul': 282, 'soule': 85, 'soull': 1, 'soulle': 0, 'souȝl': 0, 'souȝle': 0, 'sovle': 0, 'sowal': 0, 'sowel': 0, 'sowele': 0, 'sowell': 0, 'sowile': 0, 'sowl': 1, 'sowle': 12, 'sowll': 0, 'sowlle': 0, 'sowul': 0, 'sowyl': 0, 'sowyll': 1, 'sowylle': 0, 'soyle': 0, 'sæul': 0, 'sæule': 0, 'sæwl': 0, 'sæwle': 0, 'zaule': 2, 'zawl': 0, 'zoal': 0, 'zoule': 0},
	'religion_n': {'ralegioun': 0, 'releegion': 0, 'relegeon': 0, 'relegion': 0, 'relegioun': 0, 'relegioune': 0, 'relegyon': 1, 'releidgeon': 0, 'reliegieoun': 1, 'religeon': 0, 'religeoun': 0, 'religeowne': 0, 'religion': 134, 'religione': 0, 'religioun': 12, 'religioune': 2, 'religiun': 7, 'religiune': 0, 'religon': 0, 'religyon': 3, 'religyone': 0, 'religyowne': 0, 'relligion': 0, 'relygeoun': 0, 'relygion': 2, 'relygione': 1, 'relygioun': 2, 'relygyon': 3, 'relygyone': 0, 'relygyoun': 0, 'relygyoune': 0, 'relygyown': 0, 'relygyowne': 0, 'relygyun': 0, 'riligioun': 0},
	'taste_n1': {'taast': 4, 'taist': 2, 'tast': 27, 'taste': 60, 'test': 0},
	'explain_v': {'explain': 63, 'explaine': 4, 'explane': 6, 'explayn': 0, 'explayne': 3},
	'prison_n': {'preason': 0, 'preasone': 0, 'preasoun': 0, 'preassoun': 0, 'preison': 0, 'preisone': 0, 'preisoun': 0, 'preissone': 0, 'preissonne': 0, 'preissoun': 0, 'presen': 0, 'presin': 0, 'preson': 1, 'presone': 0, 'presonn': 0, 'presonne': 0, 'presoun': 0, 'presoune': 0, 'presown': 0, 'presowne': 0, 'presowun': 0, 'presoyn': 0, 'presson': 0, 'pressone': 0, 'pressoun': 0, 'pressoyn': 0, 'pressun': 0, 'presun': 0, 'presune': 0, 'preysone': 0, 'preysoun': 0, 'prieson': 0, 'prisen': 0, 'prision': 0, 'prison': 51, 'prisone': 2, 'prisonne': 0, 'prisoun': 7, 'prisoune': 1, 'prisown': 0, 'prission': 0, 'prissone': 0, 'prissoun': 0, 'prissoune': 0, 'prisun': 4, 'prisund': 0, 'prisune': 2, 'prizen': 0, 'pruson': 0, 'prwsoun': 0, 'pryson': 4, 'prysone': 0, 'prysonne': 0, 'prysoun': 1, 'prysoune': 0, 'prysown': 0, 'pryssoun': 0, 'pryssune': 0, 'prysun': 0, 'prysyn': 0},
	'probability_n': {'probabilite': 2, 'probabilitie': 4, 'probability': 32, 'probabilte': 1, 'proprability': 0, 'provibility': 0},
	'excuse_n': {'escuse': 1, 'excuse': 38},
	'princess_n': {'prences': 0, 'prencess': 0, 'prencis': 0, 'prenssis': 0, 'princeis': 0, 'princes': 6, 'princess': 60, 'princesse': 7, 'princis': 0, 'prinses': 0, 'prynces': 0, 'pryncesse': 3, 'pryncis': 0, 'pryncise': 0, 'prynsace': 0, 'pryyncesse': 0},
	'learning_n': {'larnin': 1, 'learning': 33, 'leirning': 0, 'leorning': 0, 'leornung': 0, 'lerning': 0, 'lernyng': 6, 'lernynge': 3, 'lernyngh': 0, 'lernynghe': 1},
	'amuse_v': {'ammuse': 1, 'ammuze': 0, 'amuse': 44, 'amuze': 1},
	'horn_n': {'heorn': 0, 'horn': 189, 'horne': 47, 'horun': 0},
	'serenity_n': {'serenity': 19, 'serenitie': 3, 'serenyte': 1},
	'clamour_n': {'clamor': 2, 'clamore': 0, 'clamour': 21, 'clamoure': 0, 'clamur': 0, 'clamure': 0, 'claymour': 0},
	'sole_n1': {'soal': 0, 'soale': 3, 'soile': 1, 'soille': 0, 'sole': 88, 'sool': 0, 'soole': 2, 'soul': 0, 'soule': 2, 'sowle': 0, 'solle': 0},
	'loiter_v': {'leutere': 0, 'leutre': 0, 'lewtre': 0, 'loiter': 8, 'loitre': 0, 'lotere': 0, 'lowtre': 0, 'loyeter': 0, 'loyter': 7, 'loytre': 0, 'loytron': 1},
	'lancet_n': {'lancet': 7, 'lancette': 0, 'launcet': 0, 'launcette': 1, 'lawncette': 0, 'lawnset': 0},

	# ROUND 2
	'man_n1': {'mahn': 0, 'man': 600, 'mane': 2, 'mann': 7, 'manna': 2, 'manne': 3, 'maun': 0, 'min': 2, 'mon': 18, 'mone': 0, 'monn': 0, 'monna': 0, 'monne': 1, 'mun': 5},
	'bear_v1': {'bair': 0, 'baire': 1, 'bar': 0, 'bare': 16, 'bayr': 0, 'bayre': 0, 'bear': 186, 'beara': 0, 'beare': 60, 'bearre': 0, 'beear': 0, 'beer': 1, 'beere': 1, 'beir': 0, 'beire': 1, 'beoran': 0, 'beore': 1, 'ber': 8, 'beran': 6, 'bere': 42, 'berenn': 1, 'berre': 0, 'beyr': 0, 'beyre': 1, 'bieran': 0, 'biere': 0, 'biereð': 1, 'bierð': 0, 'biraþ': 0, 'bireð': 0, 'bireþ': 0, 'birð': 0, 'bore': 0, 'buere': 0, 'burr': 0, 'byran': 0, 'byrd': 0, 'byreþ': 0, 'byrð': 1, 'byrþ': 1, 'bæran': 0, 'bære': 1},
	'fresh_adj': {'ferche': 0, 'ferchs': 0, 'fers': 0, 'fersc': 3, 'fersch': 1, 'fersche': 1, 'ferse': 0, 'fersse': 0, 'ffrech': 0, 'ffresh': 0, 'ffreshe': 0, 'firesc': 0, 'firsh': 0, 'fraiche': 1, 'fraish': 0, 'frash': 0, 'freash': 0, 'frech': 1, 'freche': 3, 'frechs': 0, 'frees': 0, 'freesch': 0, 'freis': 0, 'freisch': 3, 'freische': 0, 'freish': 0, 'freishe': 0, 'freissch': 1, 'freissh': 5, 'freisshe': 1, 'frersh': 0, 'fres': 1, 'fresch': 10, 'fresche': 13, 'fresh': 279, 'freshe': 10, 'fress': 0, 'fressch': 1, 'fressche': 1, 'fresse': 0, 'fressh': 8, 'fresshe': 14, 'freys': 0, 'freysche': 0, 'freysh': 0, 'freyshe': 0, 'freyss': 1, 'freyssche': 0, 'freyssh': 0, 'freysshe': 1, 'frosch': 1, 'frosche': 1, 'frossche': 0, 'frush': 0, 'fyrsh': 0, 'uerisse': 0, 'uers': 0, 'uersc': 1, 'uerse': 1, 'uersse': 0, 'veirss': 0, 'verhs': 0, 'versch': 0, 'verss': 2, 'versse': 1, 'vresse': 0, 'vreysch': 0},
	'motion_n': {'mocien': 0, 'mocion': 7, 'mocione': 1, 'mocioun': 18, 'mocioune': 1, 'mocyon': 5, 'mocyone': 1, 'mocyoun': 2, 'moecion': 0, 'moscyoun': 1, 'moshon': 0, 'mosion': 0, 'mosioun': 0, 'motion': 177, 'motione': 3, 'motioun': 4, 'motioune': 0, 'motiown': 0, 'motiun': 0, 'motyon': 1},
	'fatal_adj': {'fatal': 44, 'fatall': 20, 'fatell': 1, 'fathel': 1},
	'credit_n': {'cradeit': 0, 'creadid': 0, 'creadit': 0, 'creaditte': 0, 'creadyt': 0, 'creadyte': 0, 'creddit': 0, 'creddite': 0, 'credeit': 0, 'credick': 0, 'credict': 0, 'credik': 0, 'credit': 294, 'credite': 22, 'creditt': 5, 'creditte': 1, 'credyt': 1, 'credyte': 3, 'credytt': 0, 'credytte': 0, 'creedet': 0, 'cridet': 0, 'crydet': 0, 'crydett': 1, 'crydite': 0},
	'shop_n': {'chap': 0, 'choap': 0, 'choip': 0, 'choipp': 0, 'choop': 0, 'chop': 0, 'chope': 1, 'chopp': 0, 'choppe': 0, 'sceoppa': 0, 'schoop': 0, 'schop': 3, 'schope': 0, 'schopp': 0, 'schoppe': 1, 'shap': 1, 'shep': 0, 'shoop': 0, 'shoope': 0, 'shop': 198, 'shope': 0, 'shopp': 3, 'shoppe': 11, 'shorp': 1, 'ssoppe': 1},
	'firm_n2': {'firm': 35, 'firme': 2},
	'remove_v': {'ramof': 0, 'ramofe': 0, 'ramouff': 0, 'ramove': 0, 'ramowe': 0, 'ramoyff': 0, 'ramuf': 0, 'ramuff': 0, 'ramuffe': 0, 'ramuif': 0, 'ramvf': 0, 'ramvif': 0, 'ramviff': 0, 'ramwif': 0, 'remeeue': 0, 'remeeve': 1, 'remefe': 1, 'remeff': 0, 'remeove': 0, 'remeue': 5, 'remeve': 11, 'remew': 0, 'remine': 0, 'remmon': 1, 'remoeue': 1, 'remoeve': 0, 'remofe': 1, 'remoff': 0, 'remoif': 0, 'remoiff': 0, 'remoive': 0, 'remooue': 4, 'remoove': 0, 'remoow': 0, 'remoue': 20, 'remouf': 0, 'remouv': 0, 'remove': 72, 'removf': 0, 'remow': 0, 'remowe': 1, 'remowff': 0, 'remowue': 0, 'remuf': 0, 'remufe': 2, 'remuff': 0, 'remuif': 1, 'remuife': 0, 'remuiff': 0, 'remuv': 1, 'remuve': 1, 'remuvie': 1, 'remvfe': 0, 'remvif': 0, 'remvwe': 0, 'remwf': 0, 'remwif': 0, 'remwife': 0, 'rumman': 0, 'rummen': 0},
	'morality_n': {'moralite': 5, 'moralitee': 6, 'moralitie': 10, 'morality': 55, 'morallite': 0, 'morallity': 3, 'morallytie': 0, 'moralte': 1, 'moraltee': 0, 'moralyte': 1, 'moralytee': 0, 'moralytye': 1},
	'crumple_v': {'cromple': 0, 'crompull': 1, 'crompyl': 0, 'crumple': 10},
	'steel_n1': {'steel': 167, 'steele': 31, 'steeli': 1, 'steell': 2, 'steelle': 0, 'steiele': 0, 'steil': 1, 'steile': 0, 'steill': 6, 'steille': 0, 'stele': 12, 'stell': 1, 'stelle': 0, 'steyle': 0, 'steyll': 1, 'stiel': 3, 'stiele': 0, 'stiell': 1, 'stile': 3, 'still': 0, 'styl': 1, 'style': 0, 'stel': 8},
	'compliance_n': {'compliance': 29, 'complyance': 9},
	'governess_n': {'gouernesse': 10, 'governes': 0, 'governess': 45, 'governesse': 5, 'governouz': 0},
	'deposit_n': {'deposit': 33, 'deposite': 6},
	'purport_n': {'pourport': 0, 'purport': 18, 'purporte': 3, 'purportie': 0, 'purpurt': 0},
	'habitable_adj': {'abitable': 1, 'habitable': 6},
	'coquettish_adj': {'coquetish': 1, 'coquettish': 8},
	'creel_n1': {'crail': 0, 'creel': 10, 'creele': 1, 'creil': 0, 'creill': 1, 'creille': 0, 'crele': 1, 'crelle': 1, 'kreil': 0, 'krele': 0},

	# ROUND 3
	'life_n': {'hlif': 0, 'layf': 0, 'layffe': 0, 'lef': 0, 'lefe': 0, 'leif': 0, 'leife': 0, 'leive': 0, 'leue': 1, 'leyf': 0, 'lief': 5, 'liefe': 0, 'lieff': 0, 'lieiw': 0, 'lieve': 0, 'lif': 41, 'life': 687, 'liff': 2, 'liffe': 1, 'liif': 1, 'lijf': 7, 'lijfe': 0, 'liue': 18, 'liuf': 0, 'live': 0, 'liyf': 0, 'liyffe': 0, 'lyef': 0, 'lyefe': 0, 'lyeff': 0, 'lyf': 20, 'lyfe': 24, 'lyff': 4, 'lyffe': 3, 'lyfve': 0, 'lyif': 0, 'lyife': 0, 'lyiff': 0, 'lyue': 9, 'lyve': 0, 'lywe': 0, 'lyyf': 0},
	'leave_v1': {'hlæfan': 0, 'lae': 0, 'laeve': 0, 'laif': 0, 'laiff': 0, 'laiue': 0, 'laive': 0, 'laue': 0, 'lave': 1, 'lawe': 0, 'lay': 0, 'layf': 0, 'layve': 0, 'le': 0, 'lea': 0, 'leab': 0, 'leabe': 0, 'leaf': 0, 'leafe': 0, 'leaff': 0, 'leaue': 47, 'leav': 1, 'leave': 246, 'leavy': 0, 'leawe': 0, 'lebe': 0, 'lee': 0, 'leeav': 0, 'leeave': 0, 'leef': 3, 'leefe': 0, 'leeue': 1, 'leeve': 2, 'lef': 7, 'lefe': 2, 'leff': 1, 'leffe': 1, 'lefue': 0, 'lefve': 0, 'leif': 4, 'leife': 0, 'leiff': 0, 'leiue': 0, 'leiv': 0, 'leive': 0, 'leiwe': 0, 'leov': 0, 'leue': 36, 'lev': 0, 'leve': 7, 'levin': 0, 'lewe': 0, 'lewiff': 0, 'ley': 0, 'leyf': 0, 'leyfe': 0, 'leyff': 0, 'leyffe': 0, 'leyiff': 0, 'leyve': 1, 'li': 0, 'liave': 0, 'lieav': 0, 'lief': 0, 'lieff': 0, 'liue': 0, 'live': 0, 'liwe': 0, 'loave': 0, 'luf': 0, 'luif': 0, 'lye': 0, 'lyue': 0, 'lyve': 0, 'læfan': 0, 'læfe': 0, 'læue': 0},
	'open_adj': {'aipen': 0, 'apen': 0, 'apin': 0, 'apne': 0, 'appen': 0, 'appin': 0, 'appne': 0, 'appyn': 0, 'hopen': 0, 'hoppyne': 0, 'hopun': 0, 'hopyn': 0, 'hopyne': 0, 'hopynne': 0, 'oopen': 0, 'open': 545, 'opene': 7, 'openn': 0, 'openne': 0, 'opin': 5, 'opine': 1, 'opinn': 0, 'opne': 0, 'opon': 3, 'opone': 0, 'opoun': 2, 'oppen': 1, 'oppin': 6, 'oppine': 1, 'oppon': 1, 'oppyn': 2, 'oppyne': 0, 'opun': 0, 'opune': 0, 'opvn': 0, 'opyn': 12, 'opyne': 1, 'opynne': 0, 'upon': 1, 'vpen': 0, 'vpon': 1, 'vppin': 0},
	'mind_n1': {'maind': 0, 'maynd': 0, 'maynde': 0, 'meand': 0, 'meend': 0, 'meende': 1, 'meinde': 0, 'mend': 2, 'mende': 10, 'meynd': 0, 'meynde': 0, 'miend': 0, 'miende': 0, 'min': 2, 'mind': 434, 'minde': 48, 'mine': 0, 'muinde': 0, 'mund': 1, 'munde': 6, 'muynde': 6, 'myend': 1, 'myende': 1, 'myn': 0, 'mynd': 33, 'myndd': 0, 'myndde': 0, 'mynde': 133, 'myne': 1, 'myynde': 0},
	'worthy_adj': {'uirthie': 0, 'virdie': 0, 'vorchty': 0, 'vordie': 0, 'vordy': 0, 'vorthi': 0, 'vorthie': 0, 'vorthty': 0, 'vorthy': 0, 'vurthye': 0, 'werthy': 1, 'whorthy': 0, 'whurthy': 0, 'wirdie': 1, 'wirdy': 0, 'wirthi': 0, 'wirthie': 0, 'wirthy': 0, 'wirtie': 0, 'woordye': 0, 'woorthie': 5, 'woorthy': 8, 'woorthye': 2, 'worchty': 0, 'worddie': 0, 'worde': 1, 'wordie': 0, 'wordy': 17, 'wordye': 0, 'worethi': 0, 'woriþi': 0, 'worthe': 1, 'worthee': 0, 'worthethy': 0, 'worthey': 0, 'worthi': 14, 'worthie': 22, 'worthti': 0, 'worthty': 0, 'worthy': 270, 'worthye': 4, 'wortie': 0, 'wortþi': 1, 'worþei': 1, 'worþi': 17, 'worþie': 1, 'worþy': 8, 'wourde': 0, 'wourdie': 0, 'wourthi': 0, 'wourthie': 1, 'wourthy': 1, 'wourþy': 1, 'wrþi': 1, 'wrþy': 0, 'wurdie': 0, 'wurdy': 0, 'wurrþi': 0, 'wurthi': 3, 'wurthy': 1, 'wurði': 3, 'wurþi': 0, 'wurþig': 0, 'wurþy': 3, 'wyrþig': 0},
	'confidence_n': {'confidence': 67, 'confidens': 0},
	'resolution_n1': {'resollowtioune': 0, 'resollution': 0, 'resolucion': 4, 'resolucioun': 6, 'resolucioune': 1, 'resolucyon': 2, 'resolucyoun': 2, 'resolution': 187, 'resolutione': 1, 'resolutioun': 0, 'resolutioune': 0, 'resolvtion': 1, 'resolwsion': 0},
	'sympathy_n': {'sympathie': 7, 'sympathy': 40, 'simpathy': 3, 'simpathie': 4},
	'moon_n1': {'meean': 0, 'meen': 0, 'meun': 0, 'meunn': 0, 'meyun': 0, 'min': 1, 'miun': 0, 'mon': 1, 'mona': 7, 'mone': 42, 'monne': 0, 'monæ': 0, 'mooin': 0, 'moon': 118, 'moone': 32, 'moune': 0, 'movne': 0, 'mowne': 0, 'moyn': 2, 'moyne': 1, 'muin': 0, 'mune': 2, 'mvne': 0, 'mwne': 0, 'myun': 0},
	'eloquence_n': {'elloquence': 0, 'eloquence': 24, 'eloquens': 1},
	'latin_adj': {'laten': 0, 'latin': 60, 'latine': 13, 'latten': 0, 'lattin': 0, 'latyn': 6, 'latyne': 0, 'latyng': 1},
	'illustrious_adj': {'illustrious': 21, 'illustrous': 0, 'illustruows': 1},
	'gross_adj': {'groce': 2, 'groiss': 0, 'groos': 4, 'groose': 0, 'gros': 4, 'grose': 8, 'gross': 158, 'grosse': 88, 'grouse': 1},
	'vivacity_n': {'vivacite': 1, 'vivacitie': 3, 'vivacity': 53, 'vivassity': 1},
	'discuss_v': {'discus': 2, 'discuse': 2, 'discuss': 22, 'discusse': 15, 'diskousse': 0, 'disscuss': 0, 'dyscus': 2, 'dyscusse': 2},
	'plague_n': {'plaage': 0, 'plaague': 0, 'plag': 0, 'plage': 15, 'plaghe': 0, 'plague': 96, 'plaidge': 0, 'plaig': 1, 'plaige': 0, 'plaigue': 0, 'plaug': 0, 'plauge': 0, 'plawgh': 0, 'plawghe': 0, 'playe': 0, 'pleag': 0, 'pleague': 0, 'pleawge': 0, 'pleg': 1, 'plege': 0, 'ploge': 1},
	'grove_n': {'grave': 0, 'grawe': 0, 'groave': 0, 'grof': 0, 'grofe': 0, 'grove': 13},
	'loan_n1': {'lan': 1, 'lane': 5, 'layne': 1, 'loan': 17, 'loane': 5, 'lon': 1, 'londe': 1, 'lone': 10, 'lonne': 1, 'loon': 0, 'loone': 5, 'lowne': 0, 'loyane': 0},
	'angle_n1': {'ancgel': 0, 'ancgil': 0, 'angel': 2, 'angell': 0, 'angil': 0, 'angle': 15, 'angul': 0, 'angylle': 1, 'hangle': 0, 'hangul': 0, 'ongel': 0, 'ongul': 1},
	'revenge_v': {'rawenge': 0, 'reuange': 0, 'reueng': 0, 'reuenge': 19, 'revainge': 0, 'revange': 0, 'reveing': 0, 'revendge': 0, 'reveng': 0, 'revenge': 41, 'reving': 0, 'reweng': 0},
	'appease_v': {'apaise': 0, 'apayse': 0, 'apeace': 0, 'apease': 2, 'apees': 1, 'apeese': 0, 'apeise': 0, 'apese': 5, 'appaise': 0, 'appayse': 1, 'appayze': 0, 'appease': 17, 'appese': 1},
	'chill_adj': {'chele': 0, 'chil': 1, 'chill': 24, 'chyll': 1, 'shill': 1, 'schill': 1, 'schil': 0},
	'sarcophagus_n': {'sarcofagus': 1, 'sarcophagus': 10},

	# ROUND 4
	'common_adj': {'coamon': 0, 'coman': 0, 'comen': 2, 'comin': 0, 'commen': 3, 'commene': 0, 'commin': 0, 'commine': 0, 'common': 217, 'commond': 0, 'commonde': 0, 'commone': 0, 'commonne': 0, 'commoun': 0, 'commound': 0, 'commoune': 1, 'commovne': 0, 'commown': 0, 'commowne': 0, 'commun': 4, 'commund': 0, 'commune': 7, 'commuyn': 1, 'commwn': 0, 'commyn': 1, 'commyne': 0, 'comon': 5, 'comone': 1, 'comonne': 0, 'comont': 0, 'comoun': 5, 'comound': 0, 'comoune': 0, 'comovn': 0, 'comovne': 0, 'comown': 0, 'comowne': 0, 'comun': 7, 'comune': 5, 'comuyn': 0, 'comvne': 1, 'comvwne': 0, 'comvyne': 0, 'comyn': 18, 'comyne': 1, 'comynne': 0, 'coummon': 0, 'covmon': 0, 'cowman': 0, 'cowmane': 0, 'cowmmoune': 0, 'cowmon': 0, 'cowmond': 0, 'cowmone': 0, 'cowmoun': 0, 'cowmoune': 0, 'cowmownd': 0, 'komune': 1, 'quomon': 0},
	'idea_n': {'aideah': 0, 'idaea': 0, 'idaia': 0, 'idaya': 0, 'idea': 160, 'ideah': 0, 'idear': 0, 'ideer': 0, 'ideie': 1, 'ydea': 1, 'ydeye': 0},
	'result_n': {'resaltt': 1, 'result': 36},
	'heavy_adj1': {'evi': 0, 'evy': 0, 'havie': 0, 'havy': 1, 'hawy': 0, 'hawye': 0, 'hayvie': 0, 'heavie': 6, 'heavy': 234, 'heavye': 0, 'hefeg': 0, 'hefeȝ': 0, 'hefig': 0, 'hefiȝ': 2, 'heve': 0, 'hevey': 0, 'hevi': 0, 'hevy': 11, 'hevye': 1, 'hewy': 3, 'hæfig': 0},
	'avoid_v': {'aduoyde': 0, 'advoid': 0, 'advoyde': 0, 'auoid': 3, 'auoide': 1, 'auoyd': 2, 'avoid': 16, 'avoide': 2, 'avoyde': 6, 'awode': 0, 'awoyde': 0},
	'castle_n': {'caastel': 0, 'castel': 14, 'castele': 0, 'castell': 11, 'castelle': 0, 'castill': 0, 'castille': 0, 'castle': 41, 'castylle': 0, 'caystelle': 0, 'kastell': 0},
	'sick_adj': {'seok': 0, 'seock': 0, 'cec': 0, 'cek': 0, 'ceke': 0, 'seac': 0, 'seak': 0, 'seake': 1, 'sec': 1, 'seek': 1, 'seeke': 1, 'seik': 4, 'sek': 3, 'seke': 20, 'seoc': 1, 'seoch': 0, 'seyk': 1, 'sic': 1, 'sick': 180, 'sicke': 23, 'sickk': 0, 'siec': 0, 'siek': 1, 'sieke': 0, 'siik': 0, 'siike': 1, 'sijk': 4, 'sijke': 0, 'sik': 3, 'sike': 1, 'sioc': 0, 'siyk': 0, 'suc': 0, 'sycke': 2, 'syike': 0, 'syk': 1, 'syke': 6, 'syyk': 0, 'sæc': 0, 'zick': 0, 'zik': 1, 'zyke': 1},
	'literary_adj': {'letterary': 0, 'literare': 1, 'literarie': 0, 'literary': 66, 'litterarie': 0, 'litterary': 1},
	'liberal_adj': {'leberale': 0, 'leberall': 0, 'leberalle': 0, 'libberall': 0, 'liberaill': 0, 'liberal': 122, 'liberale': 0, 'liberall': 20, 'liberalle': 0, 'libral': 0, 'lyberal': 2, 'lyberall': 3, 'lyberalle': 0},
	'absent_adj': {'absent': 78, 'absente': 2, 'apsent': 0, 'apseunt': 0},
	'waste_n': {'vast': 0, 'vaste': 1, 'waast': 3, 'waist': 0, 'wast': 44, 'waste': 137, 'wayste': 0},
	'egyptian_adj': {'egipcian': 1, 'egiptian': 0, 'egypcian': 0, 'egypcien': 0, 'egypcyan': 0, 'egyptian': 17, 'ægyptian': 1},
	'approve_v1': {'approove': 0, 'approuve': 0, 'approve': 15, 'aprove': 0},
	'drama_n': {'drama': 76, 'drame': 0, 'dramma': 0},
	'mission_n': {'mission': 124, 'missyon': 1},
	'abrupt_adj': {'abrupt': 61, 'abrupte': 3},
	'accordance_n': {'accordance': 30, 'accordans': 0, 'accordaunce': 3, 'acordance': 1, 'acordans': 0, 'acordaunce': 1, 'acordauns': 0, 'anecordans': 0},
	'clumsy_adj': {'clomsey': 0, 'clumbsie': 1, 'clumsie': 3, 'clumsy': 14},
	'discourage_v': {'descourage': 0, 'descouraige': 0, 'dischorage': 0, 'discoradge': 0, 'discorage': 1, 'discoridge': 0, 'discorrage': 0, 'discourage': 20, 'discourrage': 0, 'discowrage': 0, 'discurage': 0, 'dyscorage': 2, 'dyscourage': 1, 'dyscouraige': 0, 'dyscourrage': 0},
	'admiralty_n': {'admeralitie': 0, 'admeraltie': 0, 'admeralty': 0, 'admiralite': 0, 'admiralitie': 0, 'admirality': 0, 'admiralte': 3, 'admiraltie': 4, 'admiralty': 56, 'admiraltye': 1, 'admyraltie': 0, 'admyralty': 0, 'ameralte': 0, 'amiralty': 0, 'amiraltye': 1, 'ammiraltie': 0, 'ammiralty': 0, 'amralte': 0, 'amraltie': 1, 'amralty': 0, 'amrelte': 1, 'amyralte': 0},
	'terrify_v': {'tarrafy': 0, 'tarrify': 0, 'terefie': 0, 'terrefie': 0, 'terrefy': 0, 'terrefye': 0, 'terrifee': 0, 'terrifie': 3, 'terrify': 8, 'terrifye': 0, 'terryfie': 0, 'terryfy': 0, 'terryfye': 0, 'teryfie': 0, 'torrify': 0, 'turrivy': 0},
	'cedar_n': {'cedar': 10, 'ceder': 1, 'cedir': 0, 'cedor': 0, 'cedre': 5, 'cedri': 0, 'cedur': 0, 'cedyr': 0, 'cyder': 0, 'cydyr': 1, 'sydyr': 0},
	'drowned_adj': {'drownded': 1, 'drowned': 21},
	'hostel_n1': {'hostel': 11, 'hostell': 5, 'hostelle': 0, 'hostil': 1, 'hostle': 0, 'osteill': 1, 'ostel': 3, 'ostell': 0, 'osteyl': 0, 'ostle': 1},
	'avouch_v': {'advouch': 0, 'auoch': 0, 'auouch': 6, 'auouche': 2, 'auowch': 1, 'avouch': 16, 'avouche': 1},
	
	# ROUND 5
	'home_n1': {'am': 0, 'haam': 0, 'haem': 0, 'haim': 0, 'haime': 0, 'ham': 18, 'hame': 9, 'haym': 0, 'hayme': 0, 'heam': 0, 'heame': 0, 'heaum': 0, 'heeam': 0, 'heem': 0, 'hehym': 0, 'heim': 0, 'heime': 0, 'hem': 0, 'heme': 0, 'heyem': 0, 'heyime': 0, 'hiam': 0, 'him': 0, 'hime': 0, 'hoam': 0, 'hoame': 0, 'hom': 9, 'home': 430, 'hooam': 0, 'hoom': 2, 'hoome': 2, 'howm': 0, 'howme': 0, 'hum': 0, 'hume': 0, 'hwom': 0, 'hwome': 0, 'hwum': 0, 'hyem': 0, 'hyim': 0, 'hyimm': 0, 'hyme': 0, 'om': 0, 'whoam': 0, 'whoame': 0, 'whom': 1, 'whome': 1, 'whum': 0, 'wom': 0, 'yam': 0, 'yem': 0},
	'interest_n': {'enterest': 0, 'entrest': 1, 'interest': 142, 'intrest': 0, 'intrust': 0, 'interrest': 0, 'yntrest': 1, 'intriste': 0, 'jnterest': 0, 'jntrest': 0},
	'instance_n': {'instance': 53, 'instans': 0, 'instaunce': 6, 'instauns': 1},
	'observe_v': {'abserue': 0, 'abserve': 0, 'obcerue': 0, 'obsarve': 0, 'obseref': 0, 'obserf': 1, 'obserff': 0, 'obserue': 17, 'obseruue': 0, 'observe': 38, 'obserwe': 0, 'obsirue': 0, 'upserve': 1},
	'universal_adj': {'unevarsal': 0, 'uneversall': 0, 'uniuersal': 1, 'uniuersall': 0, 'uniuersalle': 0, 'uniuersele': 0, 'univarsal': 0, 'universal': 196, 'universale': 1, 'universall': 11, 'universalle': 1, 'universel': 0, 'universell': 1, 'universiel': 1, 'uniyversale': 0, 'unyuersal': 2, 'unyuersall': 0, 'unyuersel': 0, 'unyversal': 0, 'unyversale': 0, 'unyversall': 1, 'vneversall': 0, 'vniuarsal': 0, 'vniuarsall': 0, 'vniuersal': 10, 'vniuersale': 5, 'vniuersall': 36, 'vniuersalle': 0, 'vniuersel': 4, 'vniuersele': 0, 'vniuersell': 0, 'vniveersal': 0, 'vniversal': 4, 'vniversale': 0, 'vniversall': 2, 'vniversalle': 0, 'vniwersall': 0, 'vnyuersal': 5, 'vnyuersale': 0, 'vnyuersall': 2, 'vnyuersalle': 0, 'vnyuersel': 1, 'vnyuersele': 0, 'vnyuersell': 0, 'vnyversel': 0, 'wniersale': 0, 'wniuersaill': 0, 'wniuersale': 0, 'wniuersall': 0, 'wniversall': 0},
	'report_n': {'reaport': 1, 'reaporte': 0, 'reapport': 0, 'repoirt': 1, 'repoirte': 0, 'repoort': 2, 'report': 106, 'reporte': 12, 'reyport': 0},
	'enable_v': {'enable': 18, 'enhabel': 0, 'enhabile': 0, 'enhable': 0, 'inable': 6, 'inhabile': 1, 'inhable': 0},
	'obligation_n': {'abligacion': 0, 'hoblygasyon': 0, 'obbligacioun': 0, 'oblegacioun': 0, 'oblegatyon': 0, 'oblegaytion': 0, 'obligacion': 6, 'obligacione': 0, 'obligacioun': 5, 'obligacioune': 0, 'obligacon': 0, 'obligacoun': 1, 'obligacoune': 0, 'obligacyon': 0, 'obligacyoun': 0, 'obligation': 40, 'obligatione': 0, 'obligatioun': 3, 'obligatioune': 0, 'obligatiovn': 0, 'obligaton': 0, 'obligatyowne': 0, 'oblygacion': 0, 'oblygacioun': 0, 'oblygacoun': 0, 'oblygacyon': 0, 'oblygacyun': 0, 'oblygassyon': 1, 'oblygation': 1, 'oblygatioun': 0},
	'intense_adj': {'intens': 1, 'intense': 33},
	'tranquillity_n': {'tranquility': 1, 'tranquillity': 6, 'tranquillitye': 0, 'tranquillitee': 0, 'tranquilite': 1, 'tranquilitee': 0, 'tranquilitye': 0, 'tranquillitie': 0, 'tranquillite': 3, 'tranquilitie': 0},
	'wave_n': {'wave': 124, 'weave': 1, 'whave': 0},
	'loyalty_n': {'loialtie': 1, 'loialty': 0, 'loyaltee': 1, 'loyaltie': 4, 'loyalty': 15, 'loyaltye': 0, 'loyaulte': 1},
	'interpretation_n': {'enterpretacioun': 0, 'enterpreteysoun': 1, 'interpretacione': 0, 'interpretacionne': 1, 'interpretacioun': 3, 'interpretacyon': 1, 'interpretation': 16},
	'wax_n1': {'vexe': 0, 'valx': 0, 'vax': 1, 'waks': 1, 'walx': 6, 'waux': 0, 'wax': 124, 'waxche': 0, 'waxe': 17, 'weax': 0, 'wex': 9, 'wexe': 4, 'whax': 0, 'wæx': 1},
	'accommodate_v': {'accomidate': 1, 'accommadate': 0, 'accommodat': 0, 'accommodate': 88, 'accomodat': 0, 'accomodate': 4, 'acomodate': 0},
	'colleague_n': {'colege': 0, 'coliegue': 0, 'colleague': 3, 'college': 1, 'collegue': 2, 'collig': 0, 'collige': 1},
	'anatomy_n': {'anathomy': 1, 'anathomye': 1, 'anatomie': 11, 'anatomy': 32, 'anothamie': 1, 'anothomia': 0, 'anothomy': 1, 'anotomie': 0, 'anotomy': 3, 'atomy': 0},
	'mahogany_n': {'mahagony': 1, 'mahogany': 56, 'mahogena': 1, 'mahogeney': 0, 'mahogeny': 0, 'mahoggany': 0, 'mahogoney': 0, 'mahogony': 2, 'mohoconey': 0, 'mohogany': 1, 'mohogeney': 1, 'mohoggony': 1, 'mohogony': 1},
	'prejudicial_adj1': {'preiudicial': 1, 'preiudiciall': 4, 'preiudiciel': 1, 'preiudicyall': 0, 'preiuditiall': 1, 'preiudyciall': 0, 'prejudicall': 0, 'prejudiceele': 0, 'prejudicial': 15, 'prejudiciale': 0, 'prejudiciall': 0, 'prejudiciell': 1, 'prejuditial': 0, 'prejuditiall': 0, 'prejudusiall': 0, 'prejudycyall': 1, 'prejwdycyale': 0},
	'housewife_n': {'hosewif': 0, 'hosewijf': 0, 'hosewyf': 0, 'hosewyfe': 0, 'hoswif': 0, 'hoswyf': 0, 'hoswyfe': 0, 'hoswyffe': 0, 'housewif': 1, 'housewife': 17, 'housewyf': 0, 'housewyfe': 0, 'houswif': 0, 'houswife': 3, 'houswijf': 0, 'houswyf': 0, 'houswyfe': 0, 'houswyff': 1, 'houswyue': 0, 'howsewyf': 0, 'howswyf': 0, 'howswyff': 0, 'husewif': 2, 'husewijf': 0, 'husewyfe': 1, 'huswief': 0, 'huswif': 0, 'huswife': 12, 'huswiffe': 0, 'huswijf': 1, 'huswyef': 0, 'huswyf': 0, 'huswyfe': 0, 'huswyff': 0, 'huswyffe': 0, 'hwswife': 0},
	'precocity_n': {'precocitie': 1, 'precocity': 15, 'precositie': 0, 'precosity': 0},
	'mero_n': {'mero': 3, 'merou': 1},

	# ROUND 6
	'doubt_v': {'doubt': 22},
	'confess_v': {'confese': 1, 'confess': 37, 'confesse': 32, 'confessen': 2},
	'short_adj': {'chort': 0, 'sceort': 1, 'scheort': 0, 'schert': 1, 'schort': 25, 'schorte': 6, 'schorth': 1, 'schorthe': 1, 'schortt': 0, 'scort': 3, 'shert': 0, 'shorrt': 0, 'short': 610, 'shorte': 30, 'shortt': 0, 'sort': 0, 'sorte': 0, 'ssort': 2},
	'soft_adj': {'saaft': 0, 'saft': 5, 'safte': 1, 'sauft': 0, 'saufte': 0, 'sofft': 1, 'soffte': 2, 'soft': 654, 'softe': 100, 'sohte': 0, 'souffte': 0, 'soufte': 1, 'soyft': 0, 'soyfte': 0, 'zaft': 0, 'zofte': 2},
	'sweet_adj': {'squete': 0, 'sqwete': 0, 'sueit': 0, 'suet': 4, 'suete': 7, 'suette': 0, 'suiet': 0, 'suit': 0, 'suoet': 0, 'sweet': 167, 'sweete': 26, 'sweit': 4, 'sweitt': 0, 'sweote': 1, 'swet': 6, 'swete': 39, 'swett': 0, 'swette': 1, 'sweyt': 1, 'sweyte': 1, 'swiete': 0, 'swoete': 1, 'swyte': 1, 'zuete': 0},
	'sore_adj1': {'ser': 0, 'saire': 0, 'sair': 17, 'sar': 4, 'sare': 1, 'sayr': 1, 'sayre': 1, 'sear': 0, 'soir': 2, 'sooar': 0, 'soor': 1, 'soore': 2, 'sor': 2, 'sore': 132, 'sær': 1, 'zore': 1},
	'degree_n': {'decre': 0, 'degre': 16, 'degree': 66, 'degrie': 0, 'dygre': 1, 'þegre': 0},
	'step_n1': {'stap': 0, 'stape': 4, 'stapp': 0, 'steape': 0, 'step': 184, 'stepe': 1, 'stepp': 4, 'steppe': 13, 'stiape': 1, 'stæpe': 4, 'stępe': 0},
	'village_n': {'vilage': 0, 'villach': 0, 'village': 133, 'vylage': 0, 'vyllage': 2, 'welage': 0, 'willage': 0, 'willaige': 0, 'wylage': 1},
	'weight_n1': {'whete': 0, 'whette': 0, 'gewiht': 0, 'gewyht': 0, 'iwicht': 0, 'vecht': 1, 'veicht': 0, 'veycht': 0, 'veyght': 0, 'vycht': 1, 'waicht': 0, 'waight': 19, 'waighte': 0, 'wait': 1, 'waite': 2, 'waithe': 1, 'waycht': 0, 'wayght': 2, 'wayghte': 0, 'wayht': 1, 'wayte': 0, 'wecht': 5, 'weght': 6, 'weghte': 0, 'wehht': 0, 'weicht': 0, 'weight': 204, 'weighte': 5, 'weiht': 1, 'weit': 0, 'weite': 0, 'weiȝt': 1, 'weiȝte': 3, 'weycht': 0, 'weyght': 14, 'weyghte': 1, 'weyht': 1, 'weyhte': 4, 'weyte': 1, 'weyth': 1, 'weythe': 1, 'weyȝt': 0, 'weyȝte': 1, 'weȝt': 1, 'weȝte': 0, 'wheith': 0, 'wheyt': 0, 'wheyte': 0, 'whyght': 0, 'whyghte': 0, 'whyt': 0, 'whyte': 0, 'wight': 5, 'wighte': 1, 'wiht': 1, 'witte': 0, 'wiȝt': 2, 'wiȝte': 2, 'wyght': 2, 'wyghte': 1, 'wygthe': 1, 'wyht': 1, 'wyt': 1, 'wyte': 2, 'wythe': 0, 'wytte': 0, 'wyȝt': 1, 'wyȝte': 4},
	'iron_n1': {'ahn': 0, 'ahrn': 1, 'ahun': 0, 'airan': 0, 'airn': 3, 'airne': 0, 'airone': 0, 'arn': 0, 'arne': 0, 'ayron': 0, 'ayrun': 0, 'ayser': 1, 'earin': 0, 'earing': 0, 'earn': 0, 'eeren': 0, 'eire': 0, 'eiren': 0, 'eren': 0, 'erene': 0, 'ern': 1, 'erne': 0, 'eryn': 0, 'eyren': 0, 'eyrn': 0, 'eyron': 0, 'heren': 0, 'herne': 0, 'heyron': 1, 'hierne': 0, 'hire': 0, 'hirne': 0, 'hiron': 0, 'hisen': 0, 'hyeren': 0, 'hyren': 0, 'hyrene': 0, 'hyrn': 0, 'hyrne': 0, 'hyrone': 0, 'hyryn': 0, 'iearne': 0, 'ierell': 0, 'ieren': 0, 'ierne': 0, 'ieron': 0, 'ire': 6, 'iren': 13, 'irene': 1, 'irenn': 2, 'ireron': 0, 'ireyn': 0, 'irin': 1, 'irine': 0, 'irinn': 0, 'irn': 3, 'irne': 4, 'irnne': 1, 'iron': 207, 'irone': 0, 'ironne': 0, 'iroun': 0, 'irren': 0, 'irrne': 0, 'irron': 0, 'irun': 0, 'iryn': 1, 'iryne': 0, 'isaern': 0, 'isen': 5, 'iseren': 0, 'isern': 3, 'iserne': 0, 'isrn': 0, 'issen': 0, 'issern': 0, 'isyn': 0, 'isærn': 0, 'iun': 0, 'iurn': 0, 'iyren': 0, 'iyrne': 0, 'iyron': 0, 'iyrone': 0, 'iyryn': 0, 'jerne': 0, 'jre': 0, 'jren': 0, 'jrenne': 0, 'jrne': 0, 'jron': 0, 'orn': 0, 'yeirne': 0, 'yeren': 0, 'yerin': 0, 'yern': 1, 'yerne': 2, 'yeron': 1, 'yerryn': 0, 'yeryn': 0, 'yeryne': 0, 'yirn': 1, 'yoiran': 0, 'yoren': 0, 'yorin': 0, 'yorne': 0, 'yoron': 0, 'yr': 0, 'yre': 6, 'yren': 5, 'yrene': 0, 'yrin': 0, 'yrine': 0, 'yrn': 3, 'yrne': 1, 'yron': 12, 'yrone': 0, 'yronn': 0, 'yroun': 0, 'yrovn': 0, 'yrun': 0, 'yryn': 1, 'yryne': 0, 'yse': 1, 'ysen': 1, 'ysern': 0, 'yzen': 1, 'ȝirne': 0},
	'bank_n1': {'banc': 1, 'banck': 1, 'bancke': 0, 'bank': 70, 'banke': 21, 'bannke': 0, 'bonc': 1, 'bonk': 1, 'bonke': 0, 'bunk': 0},
	'shoulder_n': {'schildur': 0, 'schodyr': 0, 'scholder': 0, 'scholdere': 0, 'scholdren': 0, 'scholdur': 1, 'schowder': 0, 'schulder': 1, 'schuldere': 0, 'schuldir': 0, 'schuldire': 0, 'schuldre': 0, 'schuldren': 0, 'schuldur': 0, 'schuldyr': 0, 'schuldyre': 0, 'sculder': 0, 'sculderen': 0, 'sculdor': 1, 'sculdur': 1, 'scyldur': 0, 'shildur': 0, 'shoder': 0, 'sholder': 2, 'sholdere': 1, 'sholdre': 0, 'shoulder': 86, 'shouldren': 0, 'shouther': 0, 'showlder': 0, 'shuder': 0, 'shuldeir': 0, 'shulder': 1, 'shuldre': 1, 'shuldren': 1, 'shuldur': 0, 'solder': 0, 'soldre': 0, 'souldiour': 0, 'ssoldren': 1, 'sulder': 0},
	'lodging_n': {'lodging': 27, 'loggyne': 0, 'ludgene': 1, 'lugin': 0, 'luging': 1, 'lugyne': 1},
	'trick_n': {'trick': 96, 'tricke': 19, 'trik': 1, 'trike': 1},
	'wing_n': {'weng': 0, 'weyng': 1, 'weynge': 3, 'whenge': 0, 'whing': 1, 'whyng': 0, 'whynge': 0, 'wing': 190, 'winge': 3, 'wyng': 7, 'wynge': 12, 'wynke': 0},
	'deer_n': {'deare': 0, 'deer': 4, 'deere': 4, 'deir': 1, 'deor': 3, 'der': 5, 'dere': 3, 'deure': 0, 'dier': 0, 'diere': 0, 'dor': 1, 'duer': 0, 'dur': 1, 'dure': 1, 'dær': 1, 'theer': 0},
	'vow_n': {'vowhe': 0, 'uuou': 0, 'voo': 0, 'vou': 2, 'voue': 0, 'vow': 38, 'vowe': 11, 'woue': 1, 'voye': 1, 'woe': 0, 'wou': 0, 'wov': 0, 'wow': 1, 'wowe': 0},
	'tie_n': {'tee': 1, 'teiȝ': 1, 'tey': 0, 'teȝ': 0, 'tie': 40, 'ty': 1, 'tye': 18},
	'lamb_n1': {'lam': 2, 'lamb': 31, 'lambe': 10, 'lame': 0, 'lamm': 1, 'lamme': 0, 'lamp': 1, 'lom': 0, 'lomb': 4, 'lombbe': 0, 'lombe': 3, 'lombor': 0, 'lome': 0, 'loom': 0, 'loomb': 1, 'loombe': 0, 'lowmpe': 0, 'lęmb': 0},
	'strife_n': {'strief': 0, 'strif': 12, 'strife': 42, 'striff': 1, 'striffe': 1, 'striif': 1, 'strijf': 1, 'strijfe': 0, 'strive': 0, 'stryf': 6, 'stryfe': 7, 'stryff': 2, 'stryffe': 1, 'stryif': 0, 'stryiff': 0, 'stryve': 1, 'strywe': 0},
	'bowl_n1': {'boal': 0, 'bole': 5, 'boll': 4, 'bolla': 1, 'bolle': 9, 'boole': 1, 'boul': 1, 'boule': 2, 'bowl': 26, 'bowle': 2},
	'wolf_n': {'wlf': 1, 'uulf': 0, 'volf': 1, 'volue': 0, 'vuolfe': 1, 'wlfe': 0, 'wolf': 63, 'wolfe': 18, 'wolff': 0, 'wolffe': 2, 'wolph': 0, 'wolphe': 0, 'woof': 1, 'woolf': 2, 'woolfe': 6, 'wouf': 0, 'wouff': 0, 'woulf': 0, 'woulfe': 4, 'wowf': 2, 'wulf': 12, 'wulfe': 2, 'wulff': 0},
	'echo_n': {'eccho': 12, 'ecco': 2, 'echo': 36, 'ecko': 1},
	'stockfish_n': {'stockfhis': 0, 'stockfihs': 0, 'stockfisch': 0, 'stockfische': 0, 'stockfish': 9, 'stockfys': 0, 'stockphyshe': 0},
	'fucus_n': {'fucus': 14, 'fukes': 3},
	'ellipsis_n': {'elipsis': 0, 'elleipsis': 0, 'ellipsis': 10, 'illipsis': 1},
	'conversazione_n': {'conversatione': 0, 'conversazione': 6},

	# ROUND 7
	'take_v': {'ta': 21, 'taa': 0, 'taak': 1, 'taake': 1, 'taas': 0, 'taayke': 0, 'tac': 5, 'tacan': 2, 'tace': 1, 'tack': 1, 'tacke': 0, 'tae': 0, 'taen': 1, 'taick': 0, 'taigh': 0, 'taik': 0, 'taike': 2, 'tais': 0, 'taiuk': 0, 'tak': 45, 'take': 1894, 'taken': 410, 'takenn': 14, 'takk': 0, 'takke': 0, 'talke': 1, 'tan': 10, 'tane': 7, 'tas': 5, 'tase': 2, 'tasse': 0, 'tatȝ': 0, 'tauk': 0, 'tay': 2, 'tayk': 0, 'tays': 0, 'teak': 1, 'teake': 0, 'teayk': 0, 'teck': 1, 'tee': 0, 'teeak': 2, 'teik': 0, 'tek': 5, 'tekky': 0, 'teuk': 0, 'tey': 0, 'teyk': 0, 'theayk': 0, 'tick': 0, 'tik': 0, 'tike': 0, 'to': 64, 'too': 0, 'tooneth': 0, 'totȝ': 0, 'tuk': 1, 'ty': 0, 'tyek': 0, 'tæce': 0},
	'grace_n': {'crace': 0, 'garace': 0, 'graace': 0, 'graas': 0, 'grace': 396, 'gracy': 0, 'graice': 0, 'grais': 0, 'graise': 0, 'gras': 3, 'grase': 2, 'grass': 0, 'grays': 0, 'graz': 0, 'graze': 0, 'greace': 0, 'grease': 0, 'greeas': 0, 'greease': 0, 'gres': 0},
	'worth_n1': {'uort': 0, 'virth': 0, 'vord': 0, 'vorth': 0, 'vortht': 0, 'vyrt': 0, 'warth': 0, 'weord': 0, 'weorð': 2, 'weorþ': 0, 'weorþe': 2, 'werthe': 1, 'werþe': 2, 'wiorð': 0, 'wiorþ': 0, 'wirth': 0, 'woorth': 3, 'woorthe': 0, 'worcht': 0, 'worrth': 0, 'worth': 145, 'worthe': 11, 'wortht': 0, 'wortth': 0, 'worz': 0, 'worð': 0, 'worþ': 5, 'worȝ': 1, 'wourcht': 0, 'wourth': 0, 'wourthe': 0, 'wrocht': 0, 'wrth': 0, 'wurd': 0, 'wurth': 0, 'wurthe': 1, 'wurð': 2, 'wurþ': 1, 'wyrth': 0, 'wyrtht': 0, 'wyrð': 0, 'wyrþ': 0},
	'depart_v': {'depairt': 1, 'depart': 30, 'departe': 24, 'deperte': 0},
	'operate_v': {'operat': 0, 'operate': 34, 'opperate': 1},
	'merriment_n': {'merement': 1, 'meriment': 3, 'merimente': 0, 'merriment': 11, 'merryment': 0, 'meryement': 0, 'meryment': 0, 'mirriement': 0, 'mirriment': 0},
	'cruise_n': {'cruise': 13, 'cruize': 2},
	'gamester_n': {'gaaymester': 0, 'gaimster': 0, 'gamester': 24, 'gamster': 1, 'geamster': 0, 'gemster': 0},
	'comedian_n': {'comedean': 0, 'comedian': 28, 'comediane': 0, 'comedien': 0, 'commedian': 0, 'commoedian': 0, 'comoedian': 0},
}


def json_read(input_file):
	with open(input_file) as file:
		data = json.load(file)
	return data

def test_all():
	for lemma, variant_counts_expected in EXPECTED_COUNTS.items():
		variant_counts_expected = sorted([(v, c) for v, c in variant_counts_expected.items()])
		lemma_data = json_read(OED_DATA / f'{lemma}.json')['variants']
		variant_counts = sorted([(v, len(data['quotations'])) for v, data in lemma_data.items()])
		assert variant_counts == variant_counts_expected
