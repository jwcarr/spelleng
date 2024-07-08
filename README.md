SpellEng
========

This repository contains data and code for the SpellEng database – a diachronic database of English spelling variation.


tl;dr
-----

- If you just want to get your hands on a CSV file, see `data/exp.csv`

- If you want to look at the statistical models, see `code/fit_models.py`

- If you want to see how the figures were made, see `code/build_figures.py`

- If you want to inspect the experiment code, see `experiment/server.js` and `experiment/client/client.js`

- If you want to listen to the spoken word forms, see `experiment/client/words/`


Organization
------------

The top-level structure of the repo is organized into:

- `code/`: Python analysis code

- `data/`: JSON and CSV data files, and NetCDF model result archives

- `manuscript/`: LaTeX manuscript and figures


Replicating the analyses
------------------------

To dive into full replication, I would recommend that you first replicate my Python 3.11 environment. First, clone or download this repository and `cd` into the top-level directory:

```bash
$ cd path/to/hethom/
```

The exact version numbers of the Python packages I used are documented in `requirements.txt`. To replicate this environment and ensure that the required packages do not interfere with your own projects, create and activate a new Python virtual environment. Here's one way to do this:

```bash
$ python3 -m venv hethom_env
$ source hethom_env/bin/activate
```

With the new environment activated, install the required Python packages from `requirements.txt`:

```bash
$ pip install --upgrade pip
$ pip install -r requirements.txt
```


Reproducible analysis pipeline
------------------------------

All intermediate and processed data files are included in this repo, so it it not necessary to reproduce all these steps unless you need to. The raw data files produced by the experiment are located in `data/exp/`. This raw data went through the following pipeline:

RAW DATA FILES -> process_exp_data.py -> EXP.JSON -> build_csv.py -> EXP.CSV -> fit_models.py -> \*.NETCDF -> build_figures.py

- `process_exp_data.py` reduces the raw data into a single JSON file that contains only the most important information (essentially just the lexicon produced by each generation, arranged into conditions and chains). If you need to access other data, you may need to refer to the raw files themselves.

- `build_csv.py` takes the JSON output of the previous step and run various measures, most importantly communicative cost. These results are output to a CSV file for analysis.

- `fit_models.py` uses the CSV file generated in the previous step and fits the statistical models. The results are stored in NetCDF files under `data/models/`.

- `build_figures.py` uses the data files generated in previous steps to create all the figures for the manuscript.



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
