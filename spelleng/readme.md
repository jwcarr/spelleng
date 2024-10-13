SpellEng: A diachronic dataset of English spelling variants
===========================================================

SpellEng consists of three UTF-8-encoded CSV files, each containing a different set of counts:

- `spelling_v1_quote.csv`: OED quotation count
- `spelling_v1_text.csv`:  Corpus text count
- `spelling_v1_token.csv`: Corpus token count

Each file contains the same 112,080 variants for the same 32,264 lemmata in the same order. Note
that the dataset contains the string "null" which some software will interpret as a null value.


Column headers
--------------

- `lemma`: OED lemma ID. Unique to each lemma. Consists of the headword, part of speech, and in some
  cases a headword number. `aaron_n1` corresponds to https://www.oed.com/dictionary/aaron_n1
- `headword`: Headword form or modern spelling. Not unique to each lemma.
- `pos`: Part of speech, which is one of `nn` noun, `vb` verb, `jj` adjective, or `rb` adverb.
- `variant`: Variant spelling. Each variant is on a separate row.
- `band1` ... `band13`: Frequency of the variant spelling during each Band's period (see below).
- `oe`: Frequency of the variant spelling in Old English (sum of Bands 1, 2, and 3).
- `me`: Frequency of the variant spelling in Middle English (sum of Bands 4, 5, 6, and 7).
- `eme`: Frequency of the variant spelling in Early Modern English (sum of Bands 8, 9, and 10).
- `lme`: Frequency of the variant spelling in Late Modern English (sum of Bands 11, 12, and 13).
- `total`: Frequency of the variant spelling across all periods (sum of Bands 1 through 13).


Historical banding
------------------

| Band | Period    | Corpus | Corpus section           | N years | N texts |   N tokens | N types |
|------|-----------|--------|--------------------------|---------|---------|------------|---------|
| 1    | Pre-950   | HCET   | Old English I & II       |   > 100 |      31 |     88,820 |  15,327 |
| 2    | 950–1049  | HCET   | Old English III          |     100 |      91 |    243,538 |  36,060 |
| 3    | 1050–1149 | HCET   | Old English IV           |     100 |      28 |     64,063 |  11,179 |
| 4    | 1150–1249 | HCET   | Middle English I         |     100 |      31 |    108,065 |  16,813 |
| 5    | 1250–1349 | HCET   | Middle English II        |     100 |      22 |     95,183 |  12,561 |
| 6    | 1350–1419 | HCET   | Middle English III       |      70 |      45 |    181,737 |  19,078 |
| 7    | 1420–1499 | HCET   | Middle English IV        |      80 |      46 |    210,988 |  23,622 |
| 8    | 1500–1569 | HCET   | Early Modern English I   |      70 |      44 |    188,709 |  19,267 |
| 9    | 1570–1639 | HCET   | Early Modern English II  |      70 |      48 |    186,920 |  16,989 |
| 10   | 1640–1709 | HCET   | Early Modern English III |      70 |      46 |    169,225 |  13,466 |
| 11   | 1710–1779 | CLMET  | Late Modern English I    |      70 |      88 | 10,351,523 |  90,928 |
| 12   | 1780–1849 | CLMET  | Late Modern English II   |      70 |      99 | 11,190,347 | 108,347 |
| 13   | 1850–1919 | CLMET  | Late Modern English III  |      70 |     143 | 12,440,365 | 116,911 |


More information
----------------

- Preprint: https://doi.org/10.31234/osf.io/kaqgf
- OSF repository: https://osf.io/jtb4m/
- GitHub repository: https://github.com/jwcarr/spelleng


Citation
--------

Carr, J. W., & Rastle, K. (2024). Frequency-dependent selection in the English spelling system
across 1000 years of history. *PsyArXiv*. Version 1.

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

License
-------

This work is licensed under Creative Commons Attribution 4.0 International. To view a copy of this
license, visit https://creativecommons.org/licenses/by/4.0/ The license requires that reusers give
credit to the creator. It allows reusers to distribute, remix, adapt, and build upon the material
in any medium or format, even for commercial purposes.
