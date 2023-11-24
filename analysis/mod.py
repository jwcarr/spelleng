from utils import json_read
import numpy as np
import pymc as pm
import arviz as az


def roulette_wheel(distribution):
	'''
	Sample an index from a frequency distribution.
	'''
	distribution = distribution / distribution.sum()
	random_prob = np.random.random()
	summation = distribution[0]
	for i in range(1, len(distribution)):
		if random_prob < summation:
			return i - 1
		summation += distribution[i]
	return i

def generate(input_dist, s, i):
	zero_indices = np.where(input_dist == 0)[0]
	p = input_dist ** s
	p = p / p.sum()
	d = np.zeros(len(input_dist), dtype=int)
	for _ in range(input_dist.sum()):
		if len(zero_indices) > 0 and np.random.random() < i:
			d[np.random.choice(zero_indices)] += 1
		else:
			d[roulette_wheel(p)] += 1
	return d

def generate_dataset(n_gens):
	dists = [np.array([10, 5, 2], dtype=int), ]
	for _ in range(n_gens):
		dists.append(
			generate(dists[-1], s=1.0, i=0.2)
		)
	return dists

def iter_pairs(l):
	for i in range(len(l) - 1):
		yield l[i], l[i + 1]

def segment_dataset_by_zeros(I, O):
	zero_indices = np.where(I == 0)[0]
	nonzero_indices = np.where(I > 0)[0]
	return I[nonzero_indices], I[zero_indices], O[nonzero_indices], O[zero_indices]


if __name__ == '__main__':

	# data = [
	# 	[pair for pair in iter_pairs(generate_dataset(10))]
	# 	for _ in range(10)
	# ]

	dataset = json_read('../data/freq_dist.json')

	coords = {
		'band': list(range(1, 11))
	}

	with pm.Model(coords=coords) as model:

		s = pm.Normal('s', 1, 2, dims='band')
		i = pm.Beta('i', alpha=1, beta=1, dims='band')

		for l, lexeme in enumerate(dataset):

			freq_dist = np.array(dataset[lexeme]['freq_dist'], dtype=int)

			freq_dist_input = freq_dist[:-1, :]
			freq_dist_output = freq_dist[1:, :]

			m, n = freq_dist_input.shape
			prob_dist_input = [[None] * n for _ in range(m)]

			for b, row in enumerate(freq_dist_input):
				denom = (row ** s[b]).sum()
				n_zeros = (row == 0).sum()
				for c, cell in enumerate(row):
					if cell == 0:
						prob_dist_input[b][c] = i[b] / n_zeros
					else:
						prob_dist_input[b][c] = cell ** s[b] / denom * (1 - i[b])

			prob_dist_input = pm.math.stack([pm.math.stack(row) for row in prob_dist_input])

			pm.Multinomial(f'd{l}', n=freq_dist_output.sum(axis=1), p=prob_dist_input, observed=freq_dist_output, dims='band')

		trace = pm.sample()

	az.plot_posterior(trace, var_names=['s', 'i'])
	az.utils.plt.show()



'''
Try to make the MultiNom two dimensional to get rid of the gen loop, p and observed will be 2D nxm matrices, with the observed shifted down a row

Or, try to define a blackbox likelihood function based on definition of MN distribution, with extra q param
'''










