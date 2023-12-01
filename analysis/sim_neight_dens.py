import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import Levenshtein


plt.rcParams.update({'font.sans-serif': 'Helvetica Neue', 'font.size': 7})


alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']


def generate_zipf(n_items, alpha=1.1, to_freq=True):
	x = np.arange(1, n_items + 1)
	d = stats.zipf(alpha)
	y = d.pmf(x)
	if to_freq is False:
		return y / y.sum()
	y /= y.min()
	return np.array([int(round(i)) for i in y])

def generate_words(n_words, min_length, max_length, alpha_prob):
	words = []
	for _ in range(n_words):
		length = np.random.randint(min_length, max_length + 1)
		word = np.random.choice(alphabet, length, p=alpha_prob)
		words.append(''.join(word))
	return words

def mutate_lexicon(lexicon, entropy, alpha_prob):
	entropy_prime = entropy.copy()
	words = []
	for i, word in enumerate(lexicon):
		if np.random.random() < 0.5:
			r = np.random.randint(len(word))
			words.append(word[:r] + word[r+1:])
			entropy_prime[i] -= np.random.normal(1, 1)
		else:
			r = np.random.randint(len(word))
			words.append(word[:r] + np.random.choice(alphabet, p=alpha_prob) + word[r:])
			entropy_prime[i] += np.random.normal(1, 1)
	return words, entropy_prime

def generate_entropy_score(n_items):
	return np.random.random(n_items) * 3

def n_dens(lexicon):
	density = []
	for word1 in lexicon:
		# dists = [Levenshtein.distance(word1, word2) / max(len(word1), len(word2)) for word2 in lexicon]
		dists = [Levenshtein.distance(word1, word2) for word2 in lexicon]
		density.append(sum(dists) / len(dists))
	return np.array(density)

def plot_regression_line(axis, x, y):
	lr = stats.linregress(x, y)
	x = np.linspace(*axis.get_xlim(), 10)
	y = lr.slope * x + lr.intercept
	axis.plot(x, y, color='k')


if __name__ == '__main__':

	n_words = 1000
	min_length = 3
	max_length = 10

	alpha_prob = generate_zipf(len(alphabet), to_freq=False)
	lexicon_freq_dist = generate_zipf(n_words)

	lexicon = generate_words(n_words, min_length, max_length, alpha_prob)
	entropy = generate_entropy_score(n_words)

	lexicon_prime, entropy_prime = mutate_lexicon(lexicon, entropy, alpha_prob)

	density = n_dens(lexicon)
	density_prime = n_dens(lexicon_prime)

	for word, word_prime, h, h_ in zip(lexicon, lexicon_prime, density, density_prime):
		print(f'{word.ljust(13, " ")}{word_prime}')


	entropy_change = entropy_prime - entropy
	density_change = density_prime - density
	colors = ['crimson' if len(w1) > len(w2) else 'cadetblue' for w1, w2 in zip(lexicon, lexicon_prime)]

	fig, axis = plt.subplots(1, 1, figsize=(3, 3))
	axis.scatter(density_change, entropy_change, c=colors, linewidths=0, alpha=0.5, s=4)
	plot_regression_line(axis, density_change, entropy_change)
	axis.set_xlabel('Sparsity increase from T1 to T2')
	axis.set_ylabel('Entropy increase from T1 to T2')
	fig.tight_layout()
	fig.savefig('/Users/jon/Desktop/sim_nd.pdf')
