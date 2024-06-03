from pathlib import Path
from utils import json_write


eml_columns = ['IdNum', 'Head', 'Cob', 'MorphStatus', 'Lang', 'MorphCnt', 'NVAffComp', 'Der', 'Comp', 'DerComp', 'Def', 'Imm', 'ImmSubCat', 'ImmSA', 'ImmAllo', 'ImmSubst', 'ImmOpac', 'TransDer', 'ImmInfix', 'ImmRevers', 'FlatSA', 'StrucLab', 'StrucAllo', 'StrucSubst', 'StrucOpac']


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'
SPELLENG = ROOT / 'spelleng'


PATH_TO_CELEX = Path('/Users/jon/Code/wp1/data/celex2/')

eml_data_path = PATH_TO_CELEX / 'english' / 'eml' / 'eml.cd'

with open(eml_data_path) as file:
	eml_data = [line.strip().split('\\')[:25] for line in file]

eml_data = {f'{item[0]}_{item[1]}': dict(zip(eml_columns, item)) for item in eml_data}

json_write(eml_data, DATA / 'celex_eml.json')
