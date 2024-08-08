from pathlib import Path
import numpy as np
import arviz as az
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import colormaps
from scipy import stats


plt.rcParams.update({'font.sans-serif': 'Helvetica Neue', 'font.size': 7})


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'

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


def list_lemmata(trace):
	bands = np.arange(11, 12)
	for band_i in bands:
		for n_variants in range(2, 9):
			print(f'N variants {n_variants}')
			try:
				y = trace.posterior[f's_b{band_i}_n{n_variants}'].mean(('chain', 'draw')).to_numpy()
			except ValueError:
				y = trace.posterior[f's_b{band_i}_n{n_variants}'].to_numpy()
			except KeyError:
				continue
			lemmata_indices_over_5 = np.where(s_estimates < -5)
			labels = trace.posterior[f's_b{band_i}_n{n_variants}'].coords[f'lemma_b{band_i}_n{n_variants}'].values
			print(labels[lemmata_indices_over_5])

def time_plot(axis, trace, y_range=10):
	axis.axhline(0, color='black', linewidth=0.8, linestyle='-')
	x = np.linspace(-y_range, y_range, 300)
	bands = np.arange(2, 14)
	for band_i in bands:
		μ_samples = trace.posterior[f'μ'].sel(band=band_i).to_numpy().flatten()
		μ_mean = μ_samples.mean()
		for n_variants in range(2, 9):

			try:
				y = trace.posterior[f's_b{band_i}_n{n_variants}'].mean(('chain', 'draw')).to_numpy()
			except ValueError:
				y = trace.posterior[f's_b{band_i}_n{n_variants}'].to_numpy()
			except KeyError:
				continue

			jitter = (np.random.random(len(y)) - 0.5) * 0.3
			x = jitter + band_i
			axis.scatter(x, y, color=COLORS_BY_BAND[band_i - 2], s=1, alpha=0.2, edgecolor=None, linewidth=0)

			if band_i == 11 and n_variants == 4:
				business_index = trace.posterior['s_b11_n4'].coords['lemma_b11_n4'].values.tolist().index('business_n')
				axis.annotate(text='BUSINESS•N', xy=(x[business_index], y[business_index]), xytext=(9,8), arrowprops=dict(arrowstyle='->'))
			if band_i == 11 and n_variants == 2:
				precious_index = trace.posterior['s_b11_n2'].coords['lemma_b11_n2'].values.tolist().index('precious_adj')
				axis.annotate(text='PRECIOUS•ADJ', xy=(x[precious_index], y[precious_index]), xytext=(9,-8), arrowprops=dict(arrowstyle='->'))

		axis.scatter(band_i+0., μ_mean, color='black', s=6)
	axis.axvline(3.5, color='gray', linewidth=0.5, linestyle='--')
	axis.axvline(7.5, color='gray', linewidth=0.5, linestyle='--')
	axis.axvline(10.5, color='gray', linewidth=0.5, linestyle='--')
	axis.set_xlim(1.5, 13.5)
	axis.set_ylim(-y_range, y_range)
	axis.set_ylabel('Selection bias ($s$)')
	axis.set_xticks(bands)
	axis.set_xticklabels(BAND_LABELS)

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


if __name__ == '__main__':

	trace = az.from_netcdf(DATA / 'fds_model_results_reduced.netcdf')

	posterior_plot(trace, ROOT / 'manuscript' / 'figs' / 'fds_posterior.pdf')

	# list_lemmata(trace)
