import numpy as np
import pymc as pm
import arviz as az
from scipy.special import gammaln
import pytensor.tensor as pt
from utils import json_read


class NoveltyPermittingMultinomial(pt.Op):

	itypes = [pt.dmatrix]
	otypes = [pt.dscalar]

	def __init__(self, data):
		self.data = data

	def perform(self, node, inputs, outputs):
		outputs[0][0] = np.array(self.log_likelihood(*inputs[0]))

	def log_likelihood(self, s, q):
		# print(s)
		# print(q)
		# print('------')
		like = 0.0
		for i in range(len(self.data) - 1):
			P = self.data[i]
			X = self.data[i + 1]
			if P.sum() == 0 or X.sum() == 0:
				continue
			P = P ** s[i]
			P = P / P.sum()
			P = P * (1 - q[i])
			zeros = np.where(P == 0.0)[0]
			if len(zeros) > 0:
				P[zeros] = q[i] / len(zeros)
			like += gammaln(X.sum() + 1) - np.sum(gammaln(X + 1)) + np.sum(X * np.log(P))
		return like


if __name__ == '__main__':

	dataset = json_read('../data/freq_dist.json')

	coords = {'band': list(range(1, 11))}

	with pm.Model(coords=coords) as model:

		# s = pm.Truncated('s', pm.Exponential.dist(lam=1), lower=0.0, upper=10.0)

		# s = pm.Exponential('s', lam=1)
		# i = pm.Beta('i', alpha=2, beta=4)

		s = pm.Exponential('s', lam=1, dims='band')
		i = pm.Beta('i', alpha=2, beta=4, dims='band')

		for n, (lexeme, data) in enumerate(dataset.items()):
			m = np.array(data['freq_dist'], dtype=int)
			NPM = NoveltyPermittingMultinomial(m)
			theta = pt.as_tensor_variable([s, i])
			pm.Potential(f'likelihood{n}', NPM(theta))

		trace = pm.sample()

		
	az.plot_posterior(trace, var_names=['s', 'i'])
	az.utils.plt.show()
