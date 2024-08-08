SpellEng: A diachronic database of English spelling variation
=============================================================

This repository contains the SpellEng dataset and the associated code from our paper on frequency-dependent selection in the history of the English spelling system.


tl;dr
-----

- If you just want to get your hands on the SpellEng dataset, look in the `spelleng/` directory

- If you want to look at the statistical model of frequency-dependent selection, see `code/fds_model.py`

- If you want to see how the figures were made, see `code/build_figures.py`


Organization
------------

The top-level structure of the repo is organized into:

- `code/`: Python code for constructing SpellEng and running the model.

- `data/`: Various JSON data files and NetCDF model result archives. The raw corpus files and extracted OED data are not committed to this public repository for copyright reasons.

- `manuscript/`: LaTeX manuscript and figures.

- `spelleng/`: The SpellEng dataset in versioned ZIP archives.


Replicating my Python environment
---------------------------------

To dive into full replication, I would recommend that you replicate my Python 3.11 environment. First, clone or download this repository and `cd` into the top-level directory:

```bash
$ cd path/to/spelleng/
```

The exact version numbers of the Python packages I used are documented in `requirements.txt`. To replicate this environment and ensure that the required packages do not interfere with your own projects, create and activate a new Python virtual environment. Here's one way to do this:

```bash
$ python3 -m venv spelleng_env
$ source spelleng_env/bin/activate
```

With the new environment activated, install the required Python packages from `requirements.txt`:

```bash
$ pip install --upgrade pip
$ pip install -r requirements.txt
```


Reproducing the SpellEng dataset
--------------------------------

For copyright reasons, we have not included the raw corpus files and OED data in this public repository. If you want to replicate the dataset from scratch, you will first need to obtain this data.

The corpora can be obtained from https://helsinkicorpus.arts.gla.ac.uk and https://fedora.clarin-d.uni-saarland.de/clmet/clmet.html and should be placed in the `data/corpora/` directory. You will then be able to run the `code/build_corpus.py` script, which will produce a single unified corpus file (`data/corpus.json`).

Once the corpus is built, you can optionally run the `code/select_lemmata.py` script, which performs the OED queries for selecting the lemmata. Cached OED search results are included in this repository (`data/oed_search_cache.json`), as is the list of lemmata itself (`data/lemmata.json`), so this step is not strictly necessary.

To extract the OED spelling variant data, a subscription to the OED is required. Assuming you have this, you can run the `OED_extract.py` script from the command line, like so:

```bash
python code/oed_extract.py data/lemmata.json
```

This will work though all the lemmata (as selected in the previous step) in random order and distributed across multiple cores. For each lemma, the script will attempt to access the OED entry and it will cache the HTML to the `data/oed_cache/` directory. The HTML is then parsed and the extracted variants/quotations are written out to JSON files under `data/oed_data/`. This will take a long time to run and should not be done lightly, since it involves pulling several gigabytes of HTML from the OED.

Once the OED data has been obtained, you can then run the `code/build_spelleng.py` script to create the SpellEng datasets for the quotation and corpus counts.


Reproducing the model results
-----------------------------

A PyMC implementation of our Bayesian model of frequency-dependent selection can be found in `code/fds_model.py`. Running the model will take some time (approx. 30 mins.), but we include a NetCDF archive of the model results in this repository, so it's not strictly necessary to rerun the model unless you want to tweak it. Note that the NetCDF archive we provide is a reduced version of the complete model results, since the complete version is around 1.4GB. The reduced version does not include the log likelihood and all s estimates are reduced to a point value, which is sufficient for most purposes. To reproduce the plots from the NetCDF archive, run the `code/plot_fds_model.py` script.


Citing this work
----------------

Carr, J. W., & Rastle, K. (2024). Frequency-dependent selection in the English spelling system across 1000 years of history.

```bibtex
@article{Carr:2024,
author = {Carr, Jon W and Rastle, Kathleen},
title = {Frequency-dependent selection in the English spelling system across 1000 years of history},
journal = {},
year = {},
volume = {},
pages = {},
doi = {}
}
```
