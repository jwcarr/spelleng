from pathlib import Path
from utils import json_write


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'
CELEX = Path('/Users/jon/Code/wp1/data/celex2/')


esl_columns = ['IdNum', 'Head', 'Cob', 'ClassNum', 'C_N', 'Unc_N', 'Sing_N', 'Plu_N', 'GrC_N', 'GrUnc_N', 'Attr_N', 'PostPos_N', 'Voc_N', 'Proper_N', 'Exp_N', 'Trans_V', 'TransComp_V', 'Intrans_V', 'Ditrans_V', 'Link_V', 'Phr_V', 'Prep_V', 'PhrPrep_V', 'Exp_V', 'Ord_A', 'Attr_A', 'Pred_A', 'PostPos_A', 'Exp_A', 'Ord_ADV', 'Pred_ADV', 'PostPos_ADV', 'Comb_ADV', 'Exp_ADV', 'Card_NUM', 'Ord_NUM', 'Exp_NUM', 'Pers_PRON', 'Dem_PRON', 'Poss_PRON', 'Refl_PRON', 'Wh_PRON', 'Det_PRON', 'Pron_PRON', 'Exp_PRON', 'Cor_C', 'Sub_C']
eml_columns = ['IdNum', 'Head', 'Cob', 'MorphStatus', 'Lang', 'MorphCnt', 'NVAffComp', 'Der', 'Comp', 'DerComp', 'Def', 'Imm', 'ImmSubCat', 'ImmSA', 'ImmAllo', 'ImmSubst', 'ImmOpac', 'TransDer', 'ImmInfix', 'ImmRevers', 'FlatSA', 'StrucLab', 'StrucAllo', 'StrucSubst', 'StrucOpac']


def reduce_to_single_pos(d):
	new_d = {k: d[k] for k in esl_columns[:4]}
	POSs = []
	for k in esl_columns[4:]:
		if d[k] == 'Y':
			POSs.append(k.split('_')[1])
	new_d['pos'] = POSs[0] if len(POSs) > 0 else None
	return new_d

def add_missing_segmentation(d):
	if d['StrucLab']:
		return d
	d['StrucLab'] = f'({d["Head"]})[{d["pos"]}]'
	return d


esl_data_path = CELEX / 'english' / 'esl' / 'esl.cd'
with open(esl_data_path) as file:
	esl_data = [line.strip().split('\\') for line in file]
esl_data = {f'{item[0]}_{item[1]}': reduce_to_single_pos(dict(zip(esl_columns, item))) for item in esl_data}

eml_data_path = CELEX / 'english' / 'eml' / 'eml.cd'
with open(eml_data_path) as file:
	eml_data = [line.strip().split('\\')[:25] for line in file]
eml_data = {
	f'{item[0]}_{item[1]}': add_missing_segmentation(dict(zip(eml_columns, item)) | {'pos': esl_data[f'{item[0]}_{item[1]}']['pos']})
	for item in eml_data
}

json_write(eml_data, DATA / 'celex_eml.json')