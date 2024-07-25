import numpy as np
import arviz as az
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import colormaps
from scipy import stats

plt.rcParams.update({'font.sans-serif': 'Helvetica Neue', 'font.size': 7})

DIST = {
	'normal': stats.norm,
	'beta': stats.beta,
	'gamma': lambda mu, sigma: stats.gamma(mu**2/sigma**2, scale=1/(mu/sigma**2)),
	'exponential': lambda lam: stats.expon(scale=1/lam),
	'uniform': lambda lower, upper: stats.uniform(loc=lower, scale=upper - lower),
}

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

PRIORS = {
	'β': ('normal', (0, 2)),
	'ζ': ('exponential', (1,)),
	'γ': ('gamma', (2, 0.5)),
	'ξ': ('exponential', (1,)),
}

COLORS_BY_BAND = colormaps['viridis'](np.linspace(0, 1, 13))


def time_plot(axis, trace, y_range=10):
	# fig, axis = plt.subplots(1, 1, figsize=(7.48, 3))
	axis.axhline(0, color='black', linewidth=0.8, linestyle='-')
	x = np.linspace(-y_range, y_range, 300)
	bands = np.arange(2, 14)
	for band_i in bands:
		# μ_samples = trace.posterior[f'μ'].sel(band=band_i).to_numpy().flatten()
		# μ_mean = μ_samples.mean()
		# μ_hdi = az.hdi(μ_samples, hdi_prob=0.95)
		# lower, upper = float(μ_hdi[0]), float(μ_hdi[1])
		for n_variants in range(2, 9):
			try:
				s_estimates = trace.posterior[f's_b{band_i}_n{n_variants}'].mean(('chain', 'draw')).to_numpy()
			except KeyError:
				continue
			jitter = (np.random.random(len(s_estimates)) - 0.5) * 0.3
			x = jitter + band_i
			y = s_estimates
			axis.scatter(x, y, color=COLORS_BY_BAND[band_i - 2], s=1, alpha=0.2, edgecolor=None, linewidth=0)
		# axis.scatter(band_i+0., μ_mean, color='crimson', s=6)
		# axis.plot([band_i+0., band_i+0.], [lower, upper], color='crimson')
	axis.axvline(3.5, color='gray', linewidth=0.5, linestyle='--')
	axis.axvline(7.5, color='gray', linewidth=0.5, linestyle='--')
	axis.axvline(10.5, color='gray', linewidth=0.5, linestyle='--')
	axis.set_xlim(1.5, 13.5)
	axis.set_ylim(-y_range, y_range)
	axis.set_ylabel('Selection bias ($s$)')
	axis.set_xticks(bands)
	axis.set_xticklabels(BAND_LABELS)
	# fig.tight_layout()
	# fig.savefig(output_file)

def plot_posterior(axis, trace, param, xlim, by_band=False):
	x = np.linspace(*xlim, 500)
	if by_band:
		for band_i in range(2, 14):
			μ_samples = trace.posterior[param].sel(band=band_i).to_numpy().flatten()
			y = stats.gaussian_kde(μ_samples).pdf(x)
			axis.plot(x, y, color=COLORS_BY_BAND[band_i - 2], linewidth=1)
		y_min, y_max = axis.get_ylim()
		padding = (y_max - y_min) / 30.0
		for band_i in range(2, 14):
			μ_samples = trace.posterior[param].sel(band=band_i).to_numpy().flatten()
			y = stats.gaussian_kde(μ_samples).pdf(x)
			axis.text(x[ np.argmax(y)], np.max(y) + padding, f'Band {band_i}', horizontalalignment='center', color=COLORS_BY_BAND[band_i - 2])
		axis.set_ylim(y_min, y_max + 2 * padding)
	else:
		μ_samples = trace.posterior[param].to_numpy().flatten()
		y = stats.gaussian_kde(μ_samples).pdf(x)
		axis.plot(x, y, color='black', linewidth=1)
	axis.set_xlim(*xlim)
	axis.set_yticks([])
	axis.set_xlabel(f'${param}$')

def plot_prior(axis, trace, param, xlim, prior_parameterization):
	x = np.linspace(*xlim, 500)
	dist = DIST[prior_parameterization[0]](*prior_parameterization[1])
	y = dist.pdf(x)
	axis.plot(x, y, color='gray', linestyle='--', linewidth=1)

def posterior_plot(trace, output_file):
	fig = plt.figure(figsize=(7.48, 7))
	gs = gridspec.GridSpec(3, 4, figure=fig, height_ratios=[2, 1.2, 0.8])

	band_axis = fig.add_subplot(gridspec.GridSpecFromSubplotSpec(1, 1, subplot_spec=gs[0, 0:4])[0, 0])
	time_plot(band_axis, trace)

	param_axes = [
		('μ', (-2, 2), gridspec.GridSpecFromSubplotSpec(1, 1, subplot_spec=gs[1, 0:2])),
		('σ', (0, 8), gridspec.GridSpecFromSubplotSpec(1, 1, subplot_spec=gs[1, 2:4])),
		('β', (-2, 2), gridspec.GridSpecFromSubplotSpec(1, 1, subplot_spec=gs[2, 0])),
		('ζ', (0, 4), gridspec.GridSpecFromSubplotSpec(1, 1, subplot_spec=gs[2, 1])),
		('γ', (0, 4), gridspec.GridSpecFromSubplotSpec(1, 1, subplot_spec=gs[2, 2])),
		('ξ', (0, 4), gridspec.GridSpecFromSubplotSpec(1, 1, subplot_spec=gs[2, 3])),
	]
	for param, xlim, axis_gs in param_axes:
		axis = fig.add_subplot(axis_gs[0, 0])
		by_band = True if param in ['μ', 'σ'] else False
		plot_posterior(axis, trace, param, xlim, by_band)
		if param in PRIORS:
			plot_prior(axis, trace, param, xlim, PRIORS[param])
	fig.tight_layout()
	fig.savefig(output_file)

def plot_chains(trace):
	all_lemmata = []
	for b in range(2, 14):
		for n in range(2, 8):
			lemmata = trace.posterior.coords[f'lemma_b{b}_n{n}'].to_dict()['dims']


if __name__ == '__main__':

	trace = az.from_netcdf(f'../data/models/fds_token2.netcdf')

	plot_chains(trace)

	# time_plot(trace, f'../manuscript/figs/fds_estimates.pdf')
	posterior_plot(trace, f'../manuscript/figs/fds_posterior.pdf')
