import numpy as np
import pymc as pm
import arviz as az
from scipy.special import gammaln
import pytensor.tensor as pt


class NoveltyPermittingMultinomial(pt.Op):

	itypes = [pt.dvector]
	otypes = [pt.dscalar]

	def __init__(self, X, P):
		self.X = X
		self.P = P

	def perform(self, node, inputs, outputs):
		outputs[0][0] = np.array(self.log_likelihood(*inputs[0]))

	def log_likelihood(self, s, q):
		X = self.X
		P = self.P
		P = P ** s
		P = P / P.sum()
		P = P * (1 - q)
		zeros = np.where(P == 0.0)[0]
		if len(zeros) > 0:
			P[zeros] = q / len(zeros)
		return gammaln(X.sum() + 1) - np.sum(gammaln(X + 1)) + np.sum(X * np.log(P))


if __name__ == '__main__':

	with pm.Model() as model:

		s = pm.Normal('s', 1, 2)
		i = pm.Beta('i', alpha=1, beta=1)

		for n in range(20):

			P = np.array([10/15, 5/15, 0])
			X = np.array([10,    5,    2])

			NPM = NoveltyPermittingMultinomial(X, P)

			theta = pt.as_tensor_variable([s, i])
			pm.Potential(f'likelihood{n}', NPM(theta))

		trace = pm.sample()

		
	az.plot_posterior(trace, var_names=['s', 'i'])
	az.utils.plt.show()
