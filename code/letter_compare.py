from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dataset_file = Path('../spelleng/spelleng_quote.csv')
df = pd.read_csv(dataset_file, keep_default_na=False)

def prop_each(modern_char, variant_chars):
	variant_counts = [
		np.zeros(13, dtype=int)
		for _ in range(len(variant_chars))
	]
	df_modern_match = df[ df['headword'].str.startswith(modern_char) ]
	for lemma_id, subset in df_modern_match.groupby('lemma_id'):
		variants = list(subset['variant'])
		for i, variant_char in enumerate(variant_chars):
			forms = [variant for variant in variants if variant.startswith(variant_char)]
			char_subset = subset[ subset['variant'].isin(forms) ]
			counts = np.array([char_subset[f'band{i}'].sum() for i in range(1, 14)])
			variant_counts[i] += counts
	variant_counts = np.row_stack(variant_counts)
	total = variant_counts.sum(axis=0, keepdims=True)
	return variant_counts / total




fig, axes = plt.subplots(1, 2)

props = prop_each('u', ['u', 'v'])
axes[0].plot(range(1, 14), props[0], color='black')
axes[0].plot(range(1, 14), props[1], color='red')

props = prop_each('v', ['u', 'v'])
axes[1].plot(range(1, 14), props[0], color='black')
axes[1].plot(range(1, 14), props[1], color='red')

plt.show()


fig, axes = plt.subplots(1, 2)

props = prop_each('i', ['i', 'j'])
axes[0].plot(range(1, 14), props[0], color='black')
axes[0].plot(range(1, 14), props[1], color='red')

props = prop_each('j', ['i', 'j'])
axes[1].plot(range(1, 14), props[0], color='black')
axes[1].plot(range(1, 14), props[1], color='red')

plt.show()