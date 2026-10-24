"""
Corpus management, search, and statistical analysis for the Mising language.

Provides tools to load, index, query, search (concordance / KWIC, regex),
and compute statistical distributions across Mising text collections.
"""

from mising.corpus.reader import CorpusDocument, CorpusReader
from mising.corpus.manager import CorpusManager, ConcordanceLine
from mising.corpus.stats import FreqDist, compute_ngrams
from mising.corpus.sample_data import load_sample_corpus, SAMPLE_DOCUMENTS

__all__ = [
    "CorpusDocument",
    "CorpusReader",
    "CorpusManager",
    "ConcordanceLine",
    "FreqDist",
    "compute_ngrams",
    "load_sample_corpus",
    "SAMPLE_DOCUMENTS",
]
