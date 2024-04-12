from pathlib import Path
import json


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'
OED = DATA / 'oed_quotations'


EXPECTED_COUNTS = {
	# ROUND 1
	'moment_n': {'malmond': 0, 'mament': 0, 'mamonde': 0, 'mamont': 0, 'mamunt': 1, 'moment': 183, 'momente': 5, 'momentt': 0},
	'soul_n': {'saal': 1, 'sal': 1, 'sale': 0, 'sall': 2, 'salle': 1, 'saoul': 1, 'sauel': 1, 'sauele': 0, 'sauell': 0, 'sauil': 0, 'sauill': 0, 'saul': 10, 'saule': 17, 'saulen': 3, 'saull': 5, 'saulle': 0, 'sauul': 0, 'sauwel': 0, 'sauwil': 0, 'sauwl': 0, 'savl': 0, 'savle': 0, 'savll': 0, 'sawal': 0, 'sawel': 0, 'sawele': 0, 'sawell': 0, 'sawil': 1, 'sawill': 0, 'sawl': 3, 'sawle': 22, 'sawll': 1, 'sawlle': 0, 'sawol': 1, 'sawul': 1, 'sawule': 0, 'sawyl': 0, 'seawl': 0, 'seole': 0, 'shoul': 2, 'showl': 0, 'soal': 1, 'soale': 0, 'soawle': 0, 'sol': 0, 'sole': 2, 'soll': 0, 'solle': 0, 'sooal': 0, 'sool': 0, 'soole': 0, 'sooll': 0, 'souel': 0, 'souell': 0, 'soul': 282, 'soule': 86, 'soull': 1, 'soulle': 0, 'souȝl': 0, 'souȝle': 0, 'sovle': 0, 'sowal': 0, 'sowel': 0, 'sowele': 0, 'sowell': 0, 'sowile': 0, 'sowl': 1, 'sowle': 13, 'sowll': 0, 'sowlle': 0, 'sowul': 0, 'sowyl': 0, 'sowyll': 1, 'sowylle': 0, 'soyle': 0, 'sæul': 0, 'sæule': 0, 'sæwl': 0, 'sæwle': 0, 'zaule': 2, 'zawl': 0, 'zoal': 0, 'zoule': 0},
	'religion_n': {'ralegioun': 0, 'releegion': 0, 'relegeon': 0, 'relegion': 0, 'relegioun': 0, 'relegioune': 1, 'relegyon': 1, 'releidgeon': 0, 'reliegieoun': 1, 'religeon': 0, 'religeoun': 0, 'religeowne': 0, 'religion': 134, 'religione': 0, 'religioun': 12, 'religioune': 2, 'religiun': 9, 'religiune': 0, 'religon': 0, 'religyon': 3, 'religyone': 0, 'religyowne': 0, 'relligion': 0, 'relygeoun': 0, 'relygion': 2, 'relygione': 1, 'relygioun': 2, 'relygyon': 3, 'relygyone': 0, 'relygyoun': 0, 'relygyoune': 0, 'relygyown': 0, 'relygyowne': 0, 'relygyun': 0, 'riligioun': 0},
	'taste_n': {'taast': 4, 'taist': 2, 'tast': 27, 'taste': 60, 'test': 0},
	'lordship_n': {'hlaforscipe': 0, 'lauerdscape': 0, 'lauerscip': 0, 'lauerscipe': 0, 'lorchepe': 0, 'lorchipe': 1, 'lorchipp': 0, 'lorchuppe': 1, 'lordesship': 0, 'lordesshipp': 0, 'lordship': 34, 'lordyschype': 0, 'lorschip': 0, 'lorschipe': 0, 'lorshuppe': 0, 'lorshyp': 0, 'lortschyp': 0},
	'explain_v': {'explain': 63, 'explaine': 4, 'explane': 6, 'explayn': 0, 'explayne': 3},
	'prison_n': {'preason': 0, 'preasone': 0, 'preasoun': 0, 'preassoun': 0, 'preison': 0, 'preisone': 0, 'preisoun': 0, 'preissone': 0, 'preissonne': 0, 'preissoun': 0, 'presen': 0, 'presin': 0, 'preson': 1, 'presone': 0, 'presonn': 0, 'presonne': 0, 'presoun': 0, 'presoune': 0, 'presown': 0, 'presowne': 0, 'presowun': 0, 'presoyn': 0, 'presson': 0, 'pressone': 0, 'pressoun': 0, 'pressoyn': 0, 'pressun': 0, 'presun': 0, 'presune': 0, 'preysone': 0, 'preysoun': 0, 'prieson': 0, 'prisen': 0, 'prision': 0, 'prison': 51, 'prisone': 3, 'prisonne': 0, 'prisoun': 7, 'prisoune': 1, 'prisown': 0, 'prission': 0, 'prissone': 0, 'prissoun': 0, 'prissoune': 0, 'prisun': 4, 'prisund': 0, 'prisune': 2, 'prizen': 0, 'pruson': 0, 'prwsoun': 0, 'pryson': 4, 'prysone': 0, 'prysonne': 0, 'prysoun': 1, 'prysoune': 0, 'prysown': 0, 'pryssoun': 0, 'pryssune': 0, 'prysun': 0, 'prysyn': 0},
	'probability_n': {'probabilite': 2, 'probabilitie': 4, 'probability': 32, 'probabilte': 1, 'proprability': 0, 'provibility': 0},
	'excuse_n': {'escuse': 1, 'excuse': 38},
	'princess_n': {'prences': 0, 'prencess': 0, 'prencis': 0, 'prenssis': 0, 'princeis': 0, 'princes': 6, 'princess': 60, 'princesse': 7, 'princis': 0, 'prinses': 0, 'prynces': 0, 'pryncesse': 3, 'pryncis': 0, 'pryncise': 0, 'prynsace': 1, 'pryyncesse': 0},
	'learning_n': {'larnin': 1, 'learning': 33, 'leirning': 0, 'leorning': 0, 'leornung': 0, 'lerning': 1, 'lernyng': 6, 'lernynge': 3, 'lernyngh': 0, 'lernynghe': 1},
	'amuse_v': {'ammuse': 1, 'ammuze': 0, 'amuse': 44, 'amuze': 1},
	'horn_n': {'heorn': 0, 'horn': 189, 'horne': 48, 'horun': 0},
	'serenity_n': {'serenity': 19, 'serenitie': 3, 'serenyte': 1},
	'clamour_n': {'clamor': 2, 'clamore': 1, 'clamour': 21, 'clamoure': 1, 'clamur': 1, 'clamure': 0},
	'sole_n': {'soal': 2, 'soale': 3, 'soile': 1, 'soille': 0, 'sole': 88, 'sool': 0, 'soole': 2, 'soul': 0, 'soule': 2, 'sowle': 0},
	'loiter_v': {'leutere': 0, 'leutre': 0, 'lewtre': 0, 'loiter': 8, 'loitre': 0, 'loltre': 0, 'lotere': 0, 'lowtre': 0, 'loyeter': 0, 'loyter': 7, 'loytre': 0, 'loytron': 1},
	'lancet_n': {'lancet': 7, 'lancette': 0, 'launcet': 0, 'launcette': 1, 'lawncette': 0, 'lawnset': 0},

	# ROUND 2
	'man_n': {'mahn': 0, 'man': 600, 'mane': 2, 'mann': 7, 'manna': 2, 'manne': 3, 'maun': 0, 'min': 2, 'mon': 18, 'mone': 0, 'monn': 0, 'monna': 0, 'monne': 1, 'mun': 5},
	'bear_v': {'bair': 0, 'baire': 1, 'bar': 5, 'bare': 18, 'bayr': 0, 'bayre': 0, 'bear': 186, 'beara': 0, 'beare': 60, 'bearre': 0, 'beear': 0, 'beer': 1, 'beere': 1, 'beir': 1, 'beire': 1, 'beoran': 0, 'beore': 1, 'ber': 9, 'beran': 6, 'bere': 42, 'berenn': 1, 'berre': 0, 'beyr': 0, 'beyre': 1, 'bieran': 0, 'biere': 0, 'biereð': 1, 'bierð': 0, 'biraþ': 0, 'bireð': 0, 'bireþ': 0, 'birð': 0, 'bore': 2, 'buere': 0, 'burr': 0, 'byran': 0, 'byrd': 0, 'byreþ': 0, 'byrð': 1, 'byrþ': 1, 'bæran': 0, 'bære': 1},
	'fresh_adj': {'ferche': 0, 'ferchs': 0, 'fers': 0, 'fersc': 3, 'fersch': 1, 'fersche': 1, 'ferse': 0, 'fersse': 0, 'ffrech': 0, 'ffresh': 0, 'ffreshe': 0, 'firesc': 0, 'firsh': 0, 'fraiche': 1, 'fraish': 0, 'frash': 0, 'freash': 0, 'frech': 1, 'freche': 3, 'frechs': 0, 'frees': 0, 'freesch': 0, 'freis': 0, 'freisch': 3, 'freische': 0, 'freish': 0, 'freishe': 0, 'freissch': 1, 'freissh': 5, 'freisshe': 1, 'frersh': 0, 'fres': 1, 'fresch': 10, 'fresche': 13, 'fresh': 279, 'freshe': 10, 'fress': 0, 'fressch': 1, 'fressche': 1, 'fresse': 0, 'fressh': 9, 'fresshe': 14, 'freys': 0, 'freysche': 0, 'freysh': 0, 'freyshe': 0, 'freyss': 1, 'freyssche': 0, 'freyssh': 0, 'freysshe': 1, 'frosch': 1, 'frosche': 1, 'frossche': 0, 'frush': 0, 'fyrsh': 0, 'uerisse': 0, 'uers': 0, 'uersc': 1, 'uerse': 1, 'uersse': 0, 'veirss': 0, 'verhs': 0, 'versch': 0, 'verss': 2, 'versse': 1, 'vresse': 0, 'vreysch': 0},
	'motion_n': {'mocien': 0, 'mocion': 7, 'mocione': 1, 'mocioun': 18, 'mocioune': 1, 'mocyon': 5, 'mocyone': 1, 'mocyoun': 2, 'moecion': 0, 'moscyoun': 1, 'moshon': 0, 'mosion': 0, 'mosioun': 0, 'motion': 177, 'motione': 3, 'motioun': 4, 'motioune': 0, 'motiown': 0, 'motiun': 0, 'motyon': 1},
	'fatal_adj': {'fatal': 44, 'fatall': 20, 'fatell': 1, 'fathel': 1},
	'credit_n': {'cradeit': 0, 'creadid': 0, 'creadit': 0, 'creaditte': 0, 'creadyt': 0, 'creadyte': 0, 'creddit': 0, 'creddite': 0, 'credeit': 0, 'credick': 0, 'credict': 0, 'credik': 0, 'credit': 294, 'credite': 22, 'creditt': 5, 'creditte': 1, 'credyt': 1, 'credyte': 3, 'credytt': 0, 'credytte': 0, 'creedet': 0, 'cridet': 0, 'crydet': 0, 'crydett': 1, 'crydite': 0},
	'shop_n': {'chap': 0, 'choap': 0, 'choip': 0, 'choipp': 0, 'choop': 0, 'chop': 0, 'chope': 1, 'chopp': 0, 'choppe': 0, 'sceoppa': 0, 'schoop': 0, 'schop': 3, 'schope': 0, 'schopp': 0, 'schoppe': 1, 'shap': 1, 'shep': 0, 'shoop': 0, 'shoope': 0, 'shop': 198, 'shope': 0, 'shopp': 3, 'shoppe': 11, 'shorp': 1, 'ssoppe': 1},
	'firm_n': {'firm': 35, 'firme': 2},
	'remove_v': {'ramof': 0, 'ramofe': 0, 'ramouff': 0, 'ramove': 0, 'ramowe': 0, 'ramoyff': 0, 'ramuf': 0, 'ramuff': 1, 'ramuffe': 0, 'ramuif': 0, 'ramvf': 0, 'ramvif': 0, 'ramviff': 0, 'ramwif': 0, 'remeeue': 0, 'remeeve': 1, 'remefe': 1, 'remeff': 0, 'remeove': 0, 'remeue': 5, 'remeve': 11, 'remew': 0, 'remine': 0, 'remmon': 1, 'remoeue': 1, 'remoeve': 0, 'remofe': 2, 'remoff': 0, 'remoif': 0, 'remoiff': 0, 'remoive': 0, 'remooue': 4, 'remoove': 0, 'remoow': 0, 'remoue': 20, 'remouf': 0, 'remouv': 0, 'remove': 72, 'removf': 0, 'remow': 0, 'remowe': 1, 'remowff': 0, 'remowue': 0, 'remuf': 0, 'remufe': 3, 'remuff': 0, 'remuif': 1, 'remuife': 0, 'remuiff': 0, 'remuv': 1, 'remuve': 1, 'remuvie': 1, 'remvfe': 0, 'remvif': 0, 'remvwe': 0, 'remwf': 0, 'remwif': 0, 'remwife': 0, 'rumman': 0, 'rummen': 0},
	'morality_n': {'moralite': 5, 'moralitee': 6, 'moralitie': 10, 'morality': 55, 'morallite': 0, 'morallity': 3, 'morallytie': 0, 'moralte': 1, 'moraltee': 0, 'moralyte': 1, 'moralytee': 0, 'moralytye': 1},
	'crumple_v': {'cromple': 0, 'crompull': 1, 'crompyl': 0, 'crumple': 10},
	'improve_v': {'emprooue': 0, 'emproue': 0, 'emprove': 1, 'improoue': 0, 'improove': 1, 'improue': 2, 'improve': 8, 'improwe': 0, 'impruf': 0, 'inproue': 0, 'inprove': 0, 'ymprove': 0},
	'steel_n': {'steel': 167, 'steele': 31, 'steeli': 1, 'steell': 4, 'steelle': 0, 'steiele': 0, 'steil': 1, 'steile': 0, 'steill': 6, 'steille': 0, 'stele': 12, 'stell': 1, 'stelle': 0, 'steyle': 0, 'steyll': 1, 'stiel': 3, 'stiele': 0, 'stiell': 2, 'stile': 3, 'still': 1, 'styl': 1, 'style': 2},
	'compliance_n': {'compliance': 29, 'complyance': 10},
	'governess_n': {'gouernesse': 10, 'governes': 0, 'governess': 45, 'governesse': 5, 'governouz': 0},
	'lunch_n': {'lonche': 1, 'lunch': 1},
	'deposit_n': {'deposit': 33, 'deposite': 6},
	'purport_n': {'pourport': 0, 'purport': 18, 'purporte': 3, 'purportie': 0, 'purpurt': 0},
	'habitable_adj': {'abitable': 1, 'habitable': 6},
	'coquettish_adj': {'coquetish': 2, 'coquettish': 8},
	'creel_n': {'crail': 0, 'creel': 10, 'creele': 1, 'creil': 0, 'creill': 1, 'creille': 0, 'crele': 1, 'crelle': 1, 'kreil': 0, 'krele': 0},

	# ROUND 3
	'life_n': {'hlif': 0, 'layf': 0, 'layffe': 0, 'lef': 0, 'lefe': 0, 'leif': 0, 'leife': 0, 'leive': 0, 'leue': 1, 'leyf': 0, 'lief': 5, 'liefe': 0, 'lieff': 0, 'lieiw': 0, 'lieve': 0, 'lif': 41, 'life': 690, 'liff': 2, 'liffe': 1, 'liif': 1, 'lijf': 7, 'lijfe': 0, 'liue': 19, 'liuf': 0, 'live': 0, 'liyf': 0, 'liyffe': 0, 'lyef': 0, 'lyefe': 0, 'lyeff': 0, 'lyf': 20, 'lyfe': 24, 'lyff': 4, 'lyffe': 3, 'lyfve': 0, 'lyif': 0, 'lyife': 0, 'lyiff': 0, 'lyue': 9, 'lyve': 4, 'lywe': 0, 'lyyf': 0},
	'leave_v': {'hlæfan': 0, 'lae': 0, 'laeve': 0, 'laif': 0, 'laiff': 0, 'laiue': 0, 'laive': 0, 'laue': 0, 'lave': 1, 'lawe': 0, 'lay': 0, 'layf': 0, 'layve': 0, 'le': 0, 'lea': 1, 'leab': 0, 'leabe': 0, 'leaf': 0, 'leafe': 0, 'leaff': 0, 'leaue': 47, 'leav': 1, 'leave': 246, 'leavy': 0, 'leawe': 0, 'lebe': 0, 'lee': 0, 'leeav': 0, 'leeave': 0, 'leef': 3, 'leefe': 0, 'leeue': 1, 'leeve': 2, 'lef': 7, 'lefe': 2, 'leff': 1, 'leffe': 1, 'lefue': 0, 'lefve': 0, 'leif': 4, 'leife': 0, 'leiff': 0, 'leiue': 0, 'leiv': 0, 'leive': 0, 'leiwe': 0, 'leov': 0, 'leue': 36, 'lev': 0, 'leve': 7, 'levin': 0, 'lewe': 0, 'lewiff': 0, 'ley': 0, 'leyf': 0, 'leyfe': 0, 'leyff': 0, 'leyffe': 0, 'leyiff': 0, 'leyve': 1, 'li': 0, 'liave': 0, 'lieav': 0, 'lief': 0, 'lieff': 0, 'liue': 0, 'live': 0, 'liwe': 0, 'loave': 0, 'luf': 0, 'luif': 0, 'lye': 0, 'lyue': 0, 'lyve': 0, 'læfan': 0, 'læfe': 0, 'læue': 0},
	'open_adj': {'aipen': 0, 'apen': 0, 'apin': 0, 'apne': 0, 'appen': 0, 'appin': 0, 'appne': 0, 'appyn': 0, 'hopen': 0, 'hoppyne': 0, 'hopun': 0, 'hopyn': 0, 'hopyne': 0, 'hopynne': 0, 'oopen': 0, 'open': 545, 'opene': 8, 'openn': 4, 'openne': 0, 'opin': 5, 'opine': 1, 'opinn': 0, 'opne': 0, 'opon': 3, 'opone': 0, 'opoun': 2, 'oppen': 1, 'oppin': 6, 'oppine': 1, 'oppon': 1, 'oppyn': 2, 'oppyne': 0, 'opun': 0, 'opune': 0, 'opvn': 0, 'opyn': 12, 'opyne': 1, 'opynne': 0, 'upon': 1, 'vpen': 0, 'vpon': 1, 'vppin': 0},
	'mind_n': {'maind': 0, 'maynd': 0, 'maynde': 0, 'meand': 0, 'meend': 0, 'meende': 1, 'meinde': 0, 'mend': 2, 'mende': 10, 'meynd': 0, 'meynde': 0, 'miend': 0, 'miende': 0, 'min': 2, 'mind': 434, 'minde': 50, 'mine': 0, 'muinde': 0, 'mund': 1, 'munde': 6, 'muynde': 6, 'myend': 1, 'myende': 1, 'myn': 1, 'mynd': 33, 'myndd': 0, 'myndde': 0, 'mynde': 133, 'myne': 2, 'myynde': 0},
	'worthy_adj': {'uirthie': 0, 'virdie': 0, 'vorchty': 0, 'vordie': 0, 'vordy': 0, 'vorthi': 0, 'vorthie': 0, 'vorthty': 0, 'vorthy': 0, 'vurthye': 0, 'werthy': 1, 'whorthy': 0, 'whurthy': 0, 'wirdie': 1, 'wirdy': 0, 'wirthi': 0, 'wirthie': 0, 'wirthy': 0, 'wirtie': 0, 'woordye': 0, 'woorthie': 5, 'woorthy': 8, 'woorthye': 2, 'worchty': 0, 'worddie': 0, 'worde': 1, 'wordie': 0, 'wordy': 17, 'wordye': 0, 'worethi': 0, 'woriþi': 0, 'worthe': 1, 'worthee': 0, 'worthethy': 0, 'worthey': 0, 'worthi': 14, 'worthie': 22, 'worthti': 0, 'worthty': 0, 'worthy': 270, 'worthye': 4, 'wortie': 0, 'wortþi': 1, 'worþei': 1, 'worþi': 17, 'worþie': 1, 'worþy': 8, 'wourde': 0, 'wourdie': 0, 'wourthi': 0, 'wourthie': 1, 'wourthy': 1, 'wourþy': 1, 'wrþi': 1, 'wrþy': 0, 'wurdie': 0, 'wurdy': 0, 'wurrþi': 2, 'wurthi': 3, 'wurthy': 1, 'wurði': 3, 'wurþi': 0, 'wurþig': 0, 'wurþy': 3, 'wyrþig': 0},
	'confidence_n': {'confidence': 67, 'confidens': 0},
	'resolution_n': {'resollowtioune': 0, 'resollution': 0, 'resolucion': 4, 'resolucioun': 6, 'resolucioune': 1, 'resolucyon': 2, 'resolucyoun': 2, 'resolution': 187, 'resolutione': 1, 'resolutioun': 0, 'resolutioune': 0, 'resolvtion': 1, 'resolwsion': 0},
	'sympathy_n': {'sympathie': 7, 'sympathy': 40, 'simpathy': 3},
	'moon_n': {'meean': 0, 'meen': 0, 'meun': 0, 'meunn': 0, 'meyun': 0, 'min': 1, 'miun': 0, 'mon': 1, 'mona': 7, 'mone': 42, 'monne': 0, 'monæ': 0, 'mooin': 0, 'moon': 118, 'moone': 32, 'moune': 0, 'movne': 0, 'mowne': 0, 'moyn': 2, 'moyne': 1, 'muin': 0, 'mune': 2, 'mvne': 0, 'mwne': 0, 'myun': 0},
	'eloquence_n': {'elloquence': 0, 'eloquence': 24, 'eloquens': 1},
	'latin_adj': {'laten': 0, 'latin': 61, 'latine': 14, 'latten': 1, 'lattin': 0, 'latyn': 6, 'latyne': 0, 'latyng': 1},
	'illustrious_adj': {'illustrious': 21, 'illustrous': 0, 'illustruows': 1},
	'gross_adj': {'groce': 2, 'groiss': 0, 'groos': 4, 'groose': 0, 'gros': 4, 'grose': 8, 'gross': 158, 'grosse': 88, 'grouse': 1},
	'vivacity_n': {'vivacite': 1, 'vivacitie': 3, 'vivacity': 53, 'vivassity': 1},
	'discuss_v': {'discus': 2, 'discuse': 2, 'discuss': 22, 'discusse': 15, 'diskousse': 0, 'disscuss': 0, 'dyscus': 2, 'dyscusse': 2},
	'plague_n': {'plaage': 0, 'plaague': 0, 'plag': 0, 'plage': 15, 'plaghe': 0, 'plague': 96, 'plaidge': 0, 'plaig': 1, 'plaige': 0, 'plaigue': 0, 'plaug': 0, 'plauge': 0, 'plawgh': 0, 'plawghe': 0, 'playe': 0, 'pleag': 0, 'pleague': 0, 'pleawge': 0, 'pleg': 1, 'plege': 0, 'ploge': 1},
	'grove_n': {'grave': 0, 'grawe': 0, 'groave': 0, 'grof': 0, 'grofe': 0, 'grove': 13},
	'loan_n': {'lan': 1, 'lane': 5, 'layne': 1, 'loan': 17, 'loane': 5, 'lon': 1, 'londe': 1, 'lone': 10, 'lonne': 1, 'loon': 0, 'loone': 5, 'lowne': 1, 'loyane': 0},
	'angle_n': {'ancgel': 0, 'ancgil': 0, 'angel': 2, 'angell': 0, 'angil': 0, 'angle': 15, 'angul': 0, 'angylle': 1, 'hangle': 0, 'hangul': 0, 'ongel': 0, 'ongul': 1},
	'revenge_v': {'rawenge': 0, 'reuange': 0, 'reueng': 0, 'reuenge': 19, 'revainge': 0, 'revange': 0, 'reveing': 0, 'revendge': 0, 'reveng': 0, 'revenge': 41, 'reving': 0, 'reweng': 0},
	'appease_v': {'apaise': 0, 'apayse': 0, 'apeace': 0, 'apease': 2, 'apees': 1, 'apeese': 0, 'apeise': 0, 'apese': 5, 'appaise': 0, 'appayse': 1, 'appayze': 0, 'appease': 17, 'appese': 1},
	'chill_adj': {'chele': 1, 'chil': 1, 'chill': 24, 'chyll': 1, 'shill': 2, 'schill': 2, 'schil': 1},
	'dilate_v': {'deleate': 0, 'dilate': 1, 'dylate': 1, 'delate': 4},
	'sarcophagus_n': {'sarcofagus': 1, 'sarcophagus': 10},

	# ROUND 4
	'common_adj': {'coamon': 0, 'coman': 0, 'comen': 2, 'comin': 0, 'commen': 3, 'commene': 0, 'commin': 0, 'commine': 0, 'common': 217, 'commond': 0, 'commonde': 0, 'commone': 0, 'commonne': 0, 'commoun': 0, 'commound': 0, 'commoune': 1, 'commovne': 0, 'commown': 0, 'commowne': 1, 'commun': 4, 'commund': 0, 'commune': 7, 'commuyn': 1, 'commwn': 0, 'commyn': 1, 'commyne': 0, 'comon': 5, 'comone': 1, 'comonne': 0, 'comont': 0, 'comoun': 5, 'comound': 0, 'comoune': 0, 'comovn': 0, 'comovne': 0, 'comown': 0, 'comowne': 0, 'comun': 7, 'comune': 5, 'comuyn': 0, 'comvne': 1, 'comvwne': 0, 'comvyne': 0, 'comyn': 18, 'comyne': 1, 'comynne': 0, 'coummon': 0, 'covmon': 0, 'cowman': 0, 'cowmane': 0, 'cowmmoune': 0, 'cowmon': 0, 'cowmond': 0, 'cowmone': 0, 'cowmoun': 0, 'cowmoune': 0, 'cowmownd': 0, 'komune': 1, 'quomon': 0},
	'idea_n': {'aideah': 0, 'idaea': 0, 'idaia': 0, 'idaya': 0, 'idea': 160, 'ideah': 0, 'idear': 0, 'ideer': 0, 'ideie': 1, 'ydea': 1, 'ydeye': 0},
	'result_n': {'resaltt': 1, 'result': 36},
	'heavy_adj': {'evi': 0, 'evy': 0, 'havie': 0, 'havy': 1, 'hawy': 0, 'hawye': 0, 'hayvie': 0, 'heavie': 6, 'heavy': 235, 'heavye': 0, 'hefeg': 0, 'hefeȝ': 0, 'hefig': 0, 'hefiȝ': 2, 'heve': 0, 'hevey': 0, 'hevi': 0, 'hevy': 11, 'hevye': 1, 'hewy': 3, 'hæfig': 0},
	'avoid_v': {'aduoyde': 0, 'advoid': 0, 'advoyde': 0, 'auoid': 3, 'auoide': 1, 'auoyd': 2, 'avoid': 16, 'avoide': 2, 'avoyde': 6, 'awode': 0, 'awoyde': 0},
	'castle_n': {'caastel': 0, 'castel': 14, 'castele': 0, 'castell': 11, 'castelle': 0, 'castill': 0, 'castille': 0, 'castle': 41, 'castylle': 0, 'caystelle': 0, 'kastell': 0},
	'sick_adj': {'seac': 0, 'seak': 1, 'seake': 1, 'sec': 1, 'seek': 3, 'seeke': 1, 'seik': 4, 'sek': 3, 'seke': 20, 'seoc': 3, 'seock': 0, 'seok': 0, 'seyk': 1, 'sic': 1, 'sick': 181, 'sicke': 23, 'sickk': 0, 'siec': 0, 'siek': 1, 'sieke': 0, 'sijk': 4, 'sijke': 0, 'sik': 3, 'sike': 5, 'suc': 0, 'syk': 1, 'syke': 6, 'sæc': 0},
	'literary_adj': {'letterary': 0, 'literare': 1, 'literarie': 0, 'literary': 66, 'litterarie': 0, 'litterary': 1},
	'liberal_adj': {'leberale': 0, 'leberall': 0, 'leberalle': 0, 'libberall': 0, 'liberaill': 0, 'liberal': 122, 'liberale': 0, 'liberall': 20, 'liberalle': 0, 'libral': 0, 'lyberal': 2, 'lyberall': 3, 'lyberalle': 0},
	'absent_adj': {'absent': 78, 'absente': 2, 'apsent': 0, 'apseunt': 0},
	'waste_n': {'vast': 0, 'vaste': 1, 'waast': 3, 'waist': 4, 'wast': 44, 'waste': 137, 'wayste': 0},
	'egyptian_adj': {'egipcian': 1, 'egiptian': 0, 'egypcian': 0, 'egypcien': 0, 'egypcyan': 0, 'egyptian': 18, 'ægyptian': 1},
	'approve_v': {'approove': 0, 'approuve': 0, 'approve': 15, 'aprove': 0},
	'drama_n': {'drama': 76, 'drame': 0, 'dramma': 0},
	'mission_n': {'mission': 124, 'missyon': 1},
	'abrupt_adj': {'abrupt': 61, 'abrupte': 3},
	'accordance_n': {'accordance': 30, 'accordans': 0, 'accordaunce': 3, 'acordance': 1, 'acordans': 0, 'acordaunce': 1, 'acordauns': 0, 'anecordans': 0},
	'clumsy_adj': {'clomsey': 0, 'clumbsie': 1, 'clumsie': 3, 'clumsy': 14},
	'discourage_v': {'descourage': 0, 'descouraige': 0, 'dischorage': 0, 'discoradge': 0, 'discorage': 1, 'discoridge': 0, 'discorrage': 0, 'discourage': 20, 'discourrage': 0, 'discowrage': 0, 'discurage': 0, 'dyscorage': 2, 'dyscourage': 1, 'dyscouraige': 0, 'dyscourrage': 0},
	'admiralty_n': {'admeralitie': 0, 'admeraltie': 0, 'admeralty': 0, 'admiralite': 0, 'admiralitie': 0, 'admirality': 0, 'admiralte': 3, 'admiraltie': 4, 'admiralty': 57, 'admiraltye': 1, 'admyraltie': 0, 'admyralty': 0, 'ameralte': 0, 'amiralty': 0, 'amiraltye': 1, 'ammiraltie': 0, 'ammiralty': 0, 'amralte': 0, 'amraltie': 1, 'amralty': 0, 'amrelte': 1, 'amyralte': 0},
	'terrify_v': {'tarrafy': 0, 'tarrify': 0, 'terefie': 0, 'terrefie': 0, 'terrefy': 0, 'terrefye': 0, 'terrifee': 0, 'terrifie': 3, 'terrify': 8, 'terrifye': 0, 'terryfie': 0, 'terryfy': 0, 'terryfye': 0, 'teryfie': 0, 'torrify': 0, 'turrivy': 0},
	'cedar_n': {'cedar': 10, 'ceder': 1, 'cedir': 0, 'cedor': 0, 'cedre': 5, 'cedri': 0, 'cedur': 0, 'cedyr': 0, 'cyder': 0, 'cydyr': 1, 'sydyr': 0},
	'drowned_adj': {'drownded': 1, 'drowned': 21},
	'hostel_n': {'hostel': 11, 'hostell': 5, 'hostelle': 0, 'hostil': 1, 'hostle': 0, 'osteill': 1, 'ostel': 3, 'ostell': 0, 'osteyl': 0, 'ostle': 1},
	'avouch_v': {'advouch': 0, 'auoch': 0, 'auouch': 6, 'auouche': 2, 'auowch': 1, 'avouch': 16, 'avouche': 1},
	
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
