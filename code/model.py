from pathlib import Path
import pandas as pd
import numpy as np
import pymc as pm
import arviz as az


def make_frequency_matrices(df, band, max_variants, additive_smoothing, max_sample_size=None, df2=None):
	# Extract frequency distributions for lemmata where there is at least one
	# occurrence at time 1 and time 2.
	if df2 is None:
		df2 = df
	df2_grouped = df2.groupby('lemma_id')
	data = []
	for lemma_id, subset in df.groupby('lemma_id'):
		f = subset[f'band{band}'].to_numpy()
		subset2 = df2_grouped.get_group(lemma_id)
		g = subset2[f'band{band - 1}'].to_numpy(dtype=float)
		if g.sum() < 4 or f.sum() < 4:
			continue
		nonzero = np.where((f > 0) | (g > 0))
		if len(nonzero[0]) > 1:
			data.append((lemma_id, g[nonzero], f[nonzero]))
	# If max_sample_size set, pick a random subset of the lemmata.
	if max_sample_size is not None:
		np.random.shuffle(data)
		data = data[:max_sample_size]
		data.sort()
	# Create matrices for the lemmata.
	lemma_ids = []
	G = np.zeros((len(data), max_variants), dtype=float)
	F = np.zeros((len(data), max_variants), dtype=int)
	for i, (lemma_id, g, f) in enumerate(data):
		indicies_to_m_largest = np.argsort(f)[-max_variants:]
		G[i, :len(g)] = g[indicies_to_m_largest] + additive_smoothing
		F[i, :len(f)] = f[indicies_to_m_largest]
		lemma_ids.append(lemma_id)
	return F, G, lemma_ids


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
	parser.add_argument('output_dir', action='store', type=str, help='directory to store trace')
	parser.add_argument('band', action='store', type=int, help='which band number to analyze')
	args = parser.parse_args()

	band = int(args.band)
	dataset_file = Path(args.dataset_file)
	output_dir = Path(args.output_dir)
	output_file = output_dir / f'fds{band}.netcdf'

	# Check input arguments
	assert args.band >= 2 and args.band <= 13
	assert dataset_file.exists()
	assert output_dir.exists()
	assert not output_file.exists()

	# Load data and get frequency matrices
	# dataset = pd.read_csv('../spelleng/spelleng_text.csv')
	# dataset2 = pd.read_csv('../spelleng/spelleng_token.csv')

	dataset = pd.read_csv('../spelleng/spelleng_text.csv')
	dataset2 = None

	F, G, lemma_ids = make_frequency_matrices(
		dataset, band,
		max_variants=8,
		additive_smoothing=0.1,
		max_sample_size=1000,
		df2=dataset2
	)

	G_mask = (G == 0)
	G_safe = np.where(G_mask, 1, G)

	# Fit the model
	with pm.Model(coords={'lemma': lemma_ids}):

		# Priors
		μ = pm.Normal('μ', mu=0, sigma=2)
		σ = pm.Exponential('σ', lam=1)
		s = pm.Normal('s', mu=μ, sigma=σ, dims='lemma')

		# μ = pm.Normal('μ', mu=0, sigma=2)
		# s = pm.Normal('s', mu=μ, sigma=2, dims='lemma')

		# s = pm.Normal('s', mu=0, sigma=2, dims='lemma')

		# Model
		p = G_safe ** (s[:, None] + 1)
		p = pm.math.where(G_mask, 0.00001, p)
		p /= p.sum(axis=1, keepdims=True)
		α = p * G.sum(axis=1, keepdims=True)

		# Likelihood
		pm.DirichletMultinomial('F', n=F.sum(axis=1), a=α, observed=F, dims='lemma')

		# Sample posterior
		trace = pm.sample(tune=1000, draws=1000, chains=6, cores=6)
		pm.compute_log_likelihood(trace)

	# Reduce all the s estimates to point values to reduce file size
	# trace.posterior['s'] = trace.posterior['s'].mean(('chain', 'draw'))

	try:
		trace.to_netcdf(f'../data/models/fds{band}_hier.netcdf')
	except BlockingIOError:
		trace.to_netcdf(f'../data/models/fds{band}_backup.netcdf')
