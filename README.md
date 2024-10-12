Frequency-dependent selection in the English spelling system across 1000 years of history
=========================================================================================

This repository contains the SpellEng dataset and the associated code from our paper on frequency-dependent selection in the history of the English spelling system. [A preprint is currently available here](https://doi.org/10.31234/osf.io/kaqgf).


tl;dr
-----

- If you just want to get your hands on the SpellEng dataset, download [`spelleng/spelleng_v1.zip`](https://github.com/jwcarr/spelleng/raw/main/spelleng/spelleng_v1.zip)

- If you want to inspect the statistical model of frequency-dependent selection, see `code/fds_model.py`

- If you're interested in how the OED data was extracted, see `code/oed_extract.py`


Organization
------------

The top-level structure of the repo is organized into:

- `code/`: Python code for constructing SpellEng and reproducing the results reported in the paper.

- `data/`: Various data files. The raw corpus data and extracted OED data are not committed to this public repository for copyright reasons.

- `manuscript/`: LaTeX manuscript and figures.

- `spelleng/`: The SpellEng dataset in versioned ZIP archives.


Replicating my Python environment
---------------------------------

To dive into full replication, I would recommend that you replicate my Python environment. First, clone or download this repository and `cd` into the top-level directory:

```bash
$ cd path/to/spelleng/
```

The codebase was last tested in Python 3.12.7 with the package versions documented in `requirements.txt`. To replicate this environment and ensure that the required packages do not interfere with your own projects, create and activate a new Python virtual environment. Here's one way to do this:

```bash
$ python3 -m venv spelleng_env
$ source spelleng_env/bin/activate
```

With the new environment activated, install the required Python packages from `requirements.txt`:

```bash
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

If you're living in the future and can't get these old package versions installed, you could try installing the latest versions of the minimal set of packages:

```bash
$ pip install numpy scipy pandas matplotlib pymc arviz requests beautifulsoup4 lxml
```


Reproducing the SpellEng dataset
--------------------------------

For copyright reasons, we have not included the raw corpus files and OED data in this public repository. If you want to replicate the dataset from scratch, you will first need to obtain this data.

The corpora can be obtained from https://helsinkicorpus.arts.gla.ac.uk and https://fedora.clarin-d.uni-saarland.de/clmet/clmet.html and should be placed in the `data/corpora/` directory. You will then be able to run `code/build_corpus.py`, which will produce a single unified corpus file (`data/corpus.json`) in around 30 seconds. To check that your copy of the corpus matches mine, compute the MD5 hash:

```bash
md5 data/corpus.json
# should result in 59dd871bae7293b732b3781e940a7431
```

Once the corpus is built, you can optionally run `code/select_lemmata.py`, which performs the OED queries for selecting the lemmata. Cached OED search results are included in this repository (`data/oed_search_cache.json`), as is the list of lemmata itself (`data/lemmata.json`), so this step is not strictly necessary unless you want to adjust how the lemmata are selected.

To extract the OED spelling variant data, a subscription to the OED is required. Assuming you have this, you can run `oed_extract.py` from the command line, like so:

```bash
python code/oed_extract.py data/lemmata.json --n_cores 6
```

This will work though all the lemmata (as selected in the previous step) in random order and distributed across multiple cores. For each lemma, the script will attempt to access the OED entry and it will cache the HTML to the `data/oed_cache/` directory. The HTML is then parsed and the extracted variants/quotations are written out to JSON files under `data/oed_data/`. This will take a long time to run and should not be done lightly, since it involves pulling several gigabytes of HTML from the OED.

Once the OED data has been obtained, you can then run `code/build_spelleng.py` to create the SpellEng datasets for the quotation and corpus counts. This is unlikely to reproduce exactly the same counts as the official SpellEng dataset, since the OED data has almost certainly changed since our parsing in early 2024.


Reproducing the quantitative results
------------------------------------

A PyMC implementation of our Bayesian model of frequency-dependent selection can be found in `code/fds_model.py`. Running the model will take some time (~30 mins), but we include a NetCDF archive of the model results in this repository, so it's not strictly necessary to rerun the model unless you want to tweak it. Note that the NetCDF archive we provide is a reduced version of the complete model results, since the complete version is around 1.4GB. The reduced version does not include the log likelihood and all s estimates are reduced to a point value, which is sufficient for most purposes. To reproduce the plots from the NetCDF archive, run the `code/plot_fds_model.py` script.

The other figures in the manuscript can be reproduced by running `code/plot_agreement.py`, `code/plot_frequency.py`, and `code/plot_entropy.py`.


Citing this work
----------------

This work is currently under review, but for now you can cite the following preprint:

Carr, J. W., & Rastle, K. (2024). Frequency-dependent selection in the English spelling system
across 1000 years of history. *PsyArXiv*. Version 1. https://doi.org/10.31234/osf.io/kaqgf

```bibtex
@article{Carr:2024,
  author = {Carr, Jon W and Rastle, Kathleen},
  title = {Frequency-Dependent Selection in the {English} Spelling System across 1000 Years of History},
  journal = {PsyArXiv},
  year = {2024},
  pages = {Version 1},
  doi = {10.31234/osf.io/kaqgf}
}
```
