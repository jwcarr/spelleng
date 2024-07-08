from pathlib import Path
import pandas as pd
import numpy as np
from mm import make_frequency_matrices


def create_comparison_set(df):
	lemma_sets = []
	for i in range(2, 14):
		matrices_by_n_variants = make_frequency_matrices(df, i,
			min_count=5,
			max_variants=8,
			additive_smoothing=0.1,
			max_sample_size=None
		)
		n_lemmata = sum(len(lemma_ids) for n_variants, (lemma_ids, F, G) in matrices_by_n_variants.items())
		print(i, n_lemmata)
		# lemma_sets.append(set(lemma_ids))
	# common_lemmata = set.intersection(*lemma_sets)
	# return common_lemmata


# dataset_file = Path('../spelleng/spelleng_text.csv')
# dataset = pd.read_csv(dataset_file)


dataset = pd.read_csv('../spelleng/spelleng_quote.csv', keep_default_na=False)
dft = pd.read_csv('../spelleng/spelleng_text.csv', keep_default_na=False)
for band_i in range(1, 14):
	dataset[f'band{band_i}'] = dataset[f'band{band_i}'] + dft[f'band{band_i}']

print(create_comparison_set(dataset))