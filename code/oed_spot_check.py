import subprocess
from pathlib import Path
import random
import utils
import numpy as np


ROOT = Path(__file__).parent.parent.resolve()
DATA = ROOT / 'data'
OED_CACHE_DIR = DATA / 'oed_cache'


def generate_zipfian_subset_sizes(n, total_sum, alpha):
	ranks = np.arange(1, n + 1)
	probabilities = 1.0 / np.power(ranks, alpha)
	probabilities /= np.sum(probabilities)
	counts = np.round(probabilities * total_sum).astype(int)
	counts[-1] += total_sum - np.sum(counts)
	return list(reversed(counts))


def iter_subsets(lemmata, n_check_lemmata):
	n_lemmata = len(lemmata)
	break_points = generate_zipfian_subset_sizes(n_check_lemmata, n_lemmata, 1.5)
	for break_point in break_points:
		yield lemmata[:break_point]
		lemmata = lemmata[break_point:]


def choose_lemma(lemmata_subset, quotations_dir):
	random.shuffle(lemmata_subset)
	for candidate_lemma in lemmata_subset:
		lemma_path = quotations_dir / f'{candidate_lemma}.json'
		if lemma_path.exists():
			return candidate_lemma, lemma_path
	raise ValueError('No lemma available in subset')


def main(lemmata_file, quotations_dir, n_check_lemmata):
	lemmata = utils.json_read(lemmata_file)
	for lemmata_subset in iter_subsets(list(lemmata.keys()), n_check_lemmata):
		validation_lemma, lemma_path = choose_lemma(lemmata_subset, quotations_dir)
		quotation_data = utils.json_read(lemma_path)
		variant_counts = {variant: len(quotations) for variant, quotations in quotation_data.items()}
		print(validation_lemma.upper())
		print(f"'{validation_lemma}': {variant_counts},")
		subprocess.check_output(['open', '-a', 'Safari', f'file://{OED_CACHE_DIR}/{validation_lemma}.html'])
		subprocess.check_output(['open', '-a', 'Sublime Text', lemma_path])
		input()


if __name__ == '__main__':

	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('lemmata_file', action='store', type=str, help='json file listing lemmata to extract/parse')
	parser.add_argument('quotations_dir', action='store', type=str, help='directory to store json output for each lemma')
	parser.add_argument('--n_check_lemmata', action='store', type=int, default=25, help='number of lemmata to spot check')
	args = parser.parse_args()

	main(
		Path(args.lemmata_file),
		Path(args.quotations_dir),
		args.n_check_lemmata,
	)
