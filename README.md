# Russian L2 readability models

This repository contains models for automatically classifying Russian texts
according to second-language readability level (and the code used to train
them).

## Corpora

At least some of the models are based on
[this corpus](https://github.com/reynoldsnlp/rus_readability_corpus), which
cannot be shared publicly for copyright reasons. If you need access to the
corpus for research purposes, please open an issue or send me an email at
robert\_reynoldsbanana@byu.edu (but remove the tropical fruit).

## Feature extraction

The feature extraction is performed using
[udar](https://github.com/reynoldsnlp/udar), a finite-state morphological
analyzer and rule-based disambiguator for Russian.
