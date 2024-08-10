from collections import defaultdict
from pathlib import Path
import pandas as pd
import numpy as np
import pymc as pm
import arviz as az


def make_frequency_matrices(df, band, min_count, max_variants, additive_smoothing, max_sample_size=None):
	# Extract frequency distributions for lemmata where there is at least one
	# occurrence at time 1 and time 2, and at least two variants across time
	# 1 and time 2. In the number of variants is greater than max_variants,
	# take only the n most frequent variants.
	lemmata_data = []
	for lemma_id, subset in df.groupby('lemma'):
		f = subset[f'band{band}'].to_numpy()
		g = subset[f'band{band - 1}'].to_numpy(dtype=float)
		if g.sum() < min_count or f.sum() < min_count:
			continue
		nonzero = np.where((f > 0) | (g > 0))
		if len(nonzero[0]) < 2:
			continue
		f = f[nonzero]
		g = g[nonzero]
		indicies_to_n_largest = np.argsort(f)[-max_variants:]
		f = f[indicies_to_n_largest]
		g = g[indicies_to_n_largest]
		lemmata_data.append( [lemma_id, f, g] )
	# If max_sample_size is set, pick a random subset of the lemmata.
	if max_sample_size is not None:
		np.random.shuffle(lemmata_data)
		lemmata_data = lemmata_data[:max_sample_size]
		lemmata_data.sort()
	# Reorganize the data by number of variants.
	lemmata_data_by_n_variants = defaultdict(list)
	for lemma_id, f, g in lemmata_data:
		lemmata_data_by_n_variants[len(f)].append( [lemma_id, f, g] )
	# Reorganzie the data into matrices and add additive smoothing to G.
	matrices_by_n_variants = {}
	for n_variants in sorted(list(lemmata_data_by_n_variants.keys())):
		lemmata_data = lemmata_data_by_n_variants[n_variants]
		matrices_by_n_variants[n_variants] = [
			[lemma_data[0] for lemma_data in lemmata_data],
			np.array([lemma_data[1] for lemma_data in lemmata_data], dtype=int),
			np.array([lemma_data[2] for lemma_data in lemmata_data], dtype=float) + additive_smoothing
		]
	return matrices_by_n_variants


def create_comparison_set(df):
	lemma_sets = []
	for i in range(1, 13):
		lemma_ids, F0, F1 = make_frequency_matrices(df, f'band{i}', f'band{i+1}')
		lemma_sets.append(set(lemma_ids))
	common_lemmata = set.intersection(*lemma_sets)
	return common_lemmata


if __name__ == '__main__':

	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('dataset_file', action='store', type=str, help='CSV dataset file')
	parser.add_argument('output_file', action='store', type=str, help='file to store trace')
	args = parser.parse_args()

	dataset_file = Path(args.dataset_file)
	output_file = Path(args.output_file)

	# Check input arguments
	assert dataset_file.exists()
	assert not output_file.exists()

	# Load data and get frequency matrices
	dataset = pd.read_csv(dataset_file, keep_default_na=False)

	data_by_band = [
		make_frequency_matrices(
			dataset,
			band=band,
			min_count=5,
			max_variants=8,
			additive_smoothing=0.1,
			max_sample_size=None,
		)
		for band in range(2, 14)
	]

	coords = {'band': list(range(2, 14))}
	for b, matrices_by_n_variants in enumerate(data_by_band, 2):
		for n, (lemma_ids, F, G) in matrices_by_n_variants.items():
			coords[f'lemma_b{b}_n{n}'] = lemma_ids

	with pm.Model(coords=coords):

		β = pm.Normal('β', mu=0, sigma=2)
		ζ = pm.Exponential('ζ', lam=1)

		γ = pm.Gamma('γ', mu=2, sigma=0.5)
		ξ = pm.Exponential('ξ', lam=1)

		μ = pm.Normal(f'μ', mu=β, sigma=ζ, dims='band')
		σ = pm.Gamma(f'σ', mu=γ, sigma=ξ, dims='band')

		for b, matrices_by_n_variants in enumerate(data_by_band, 2):
			for n, (lemma_ids, F, G) in matrices_by_n_variants.items():
				s = pm.Normal(f's_b{b}_n{n}', mu=μ[b-2], sigma=σ[b-2], dims=f'lemma_b{b}_n{n}')
				p = G ** ( s[:, None] + 1 )
				p /= p.sum(axis=1, keepdims=True)
				α = p * G.sum(axis=1, keepdims=True)
				pm.DirichletMultinomial(f'F_b{b}_n{n}', n=F.sum(axis=1), a=α, observed=F, dims=f'lemma_b{b}_n{n}')

		trace = pm.sample(tune=1000, draws=1000, chains=6, cores=6, target_accept=0.9)
		pm.compute_log_likelihood(trace)

	trace.to_netcdf(output_file)

	# Create a second copy of the trace with the log likehood removed and the
	# s estimates reduced to point values. This copy will be committed to the
	# public repo, since the complete trace is very large (~1.4GB).
	del trace.log_likelihood
	for b, matrices_by_n_variants in enumerate(data_by_band, 2):
		for n, (lemma_ids, F, G) in matrices_by_n_variants.items():
			trace.posterior[f's_b{b}_n{n}'] = trace.posterior[f's_b{b}_n{n}'].mean(('chain', 'draw'))
	trace.to_netcdf(output_file.with_stem(f'{output_file.stem}_reduced'))
