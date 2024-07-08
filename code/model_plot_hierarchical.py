import numpy as np
import arviz as az
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde, norm, t

plt.rcParams.update({'font.sans-serif': 'Helvetica Neue', 'font.size': 7})


BAND_LABELS = [
	"Band 2\n950–1049",
	"Band 3\n1050–1149",
	"Band 4\n1150–1249",
	"Band 5\n1250–1349",
	"Band 6\n1350–1419",
	"Band 7\n1420–1499",
	"Band 8\n1500–1569",
	"Band 9\n1570–1639",
	"Band 10\n1640–1709",
	"Band 11\n1710–1779",
	"Band 12\n1780–1849",
	"Band 13\n1850–1919",
]
# BAND_LABELS = [
# 	"Band 2\nOE III\n950–1049",
# 	"Band 3\nOE IV\n1050–1149",
# 	"Band 4\nME I\n1150–1249",
# 	"Band 5\nME II\n1250–1349",
# 	"Band 6\nME III\n1350–1419",
# 	"Band 7\nME IV\n1420–1499",
# 	"Band 8\nEME I\n1500–1569",
# 	"Band 9\nEME II\n1570–1639",
# 	"Band 10\nEME III\n1640–1709",
# 	"Band 11\nLME I\n1710–1779",
# 	"Band 12\nLME II\n1780–1849",
# 	"Band 13\nLME III\n1850–1919",
# ]


def plot(y_range=10):
	
	fig, axis = plt.subplots(1, 1, figsize=(7.48, 3))
	axis.axhline(0, color='gray', linewidth=0.5, linestyle='--')

	x = np.linspace(-y_range, y_range, 300)

	bands = np.arange(2, 14)

	trace = az.from_netcdf(f'../data/models/fds_token.netcdf')

	for band_i in bands:
		μ_samples = trace.posterior[f'μ'].sel(band=band_i).to_numpy().flatten()
		μ_mean = μ_samples.mean()
		μ_hdi = az.hdi(μ_samples, hdi_prob=0.95)
		lower, upper = float(μ_hdi[0]), float(μ_hdi[1])

		for n_variants in range(2, 9):
			try:
				s_estimates = trace.posterior[f's_b{band_i}_n{n_variants}'].mean(('chain', 'draw')).to_numpy()
			except KeyError:
				continue
			jitter = (np.random.random(len(s_estimates)) - 0.5) * 0.3
			x = jitter + band_i
			y = s_estimates
			axis.scatter(x, y, color='black', s=1, alpha=0.2, edgecolor=None, linewidth=0)

		axis.scatter(band_i+0., μ_mean, color='purple', s=6)
		axis.plot([band_i+0., band_i+0.], [lower, upper], color='purple')


	axis.set_xlim(1.5, 13.5)
	axis.set_ylim(-y_range, y_range)
	axis.set_ylabel('Selection bias')
	# axis.set_xlabel('Historical band')
	axis.set_xticks(bands)
	axis.set_xticklabels(BAND_LABELS)

	fig.tight_layout()

	fig.savefig(f'../manuscript/figs/fds_token.pdf')



plot()
