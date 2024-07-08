import numpy as np
import arviz as az
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde, norm, t

plt.rcParams.update({'font.sans-serif': 'Helvetica Neue', 'font.size': 7})


BANDS = [
	"Band 2\nOE III\n950–1049",
	"Band 3\nOE IV\n1050–1149",
	"Band 4\nME I\n1150–1249",
	"Band 5\nME II\n1250–1349",
	"Band 6\nME III\n1350–1419",
	"Band 7\nME IV\n1420–1499",
	"Band 8\nEME I\n1500–1569",
	"Band 9\nEME II\n1570–1639",
	"Band 10\nEME III\n1640–1709",
	"Band 11\nLME I\n1710–1779",
	"Band 12\nLME II\n1780–1849",
	"Band 13\nLME III\n1850–1919",
]


def plot(dataset_name):
	
	fig, axis = plt.subplots(1, 1, figsize=(7.48, 3))
	axis.axhline(0, color='gray', linewidth=0.5, linestyle='--')

	x = np.linspace(-5, 5, 300)

	bands = np.arange(2, 14)

	for band_i in bands:
		print(band_i)
		try:
			trace = az.from_netcdf(f'../data/models/{dataset_name}/fds{band_i}.netcdf')
		except FileNotFoundError:
			continue
		# print(az.summary(trace, var_names=['μ', 'σ']))

		μ_samples = trace.posterior['μ'].to_numpy().flatten()
		μ_mean = μ_samples.mean()
		μ_hdi = az.hdi(μ_samples, hdi_prob=0.95)
		lower, upper = float(μ_hdi[0]), float(μ_hdi[1])

		for n_variants in range(2, 9):
			try:
				s_estimates = trace.posterior[f's{n_variants}'].mean(('chain', 'draw')).to_numpy()
			except KeyError:
				continue
				s_estimates = trace.posterior['s'].to_numpy()

			jitter = (np.random.random(len(s_estimates)) - 0.5) * 0.3

			x = jitter + band_i
			y = s_estimates

			# labelled_indices = np.random.choice(np.arange(len(x)), 10, replace=False)
			# labels = trace.posterior[f's{n_variants}'][f'lemma{n_variants}'].to_dict()['data']

			axis.scatter(x, y, color='black', s=1, alpha=0.2, edgecolor=None, linewidth=0)

		# for i in labelled_indices:
		# 	axis.text(x[i], y[i], labels[i])

		axis.scatter(band_i+0., μ_mean, color='HotPink', s=6)
		axis.plot([band_i+0., band_i+0.], [lower, upper], color='HotPink')

		# print(trace.posterior.s.sel(lemma=['woman_n']))


	axis.set_xlim(1.5, 13.5)
	axis.set_ylim(-5, 5)
	axis.set_xlabel('Historical band')
	axis.set_ylabel('Selection bias')
	axis.set_xticks(bands)
	axis.set_xticklabels(BANDS)

	fig.tight_layout()

	fig.savefig(f'../manuscript/figs/fds_results_{dataset_name}.pdf')



plot('bigquote')
plot('bigtext')

