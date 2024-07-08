import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


DIST = {
	'normal': stats.norm,
	'beta': stats.beta,
	'gamma': lambda mu, sigma: stats.gamma(mu**2/sigma**2, scale=1/(mu/sigma**2)),
	'exponential': lambda lam: stats.expon(scale=1/lam),
	'uniform': lambda lower, upper: stats.uniform(loc=lower, scale=upper - lower),
}


gamma = DIST['gamma'](3,0.5)

x = np.linspace(0, 10, 500)
y = gamma.pdf(x)

plt.plot(x, y)
plt.xlim(x[0], x[-1])
plt.show()