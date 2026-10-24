"""
Mising Natural Language Processing Library.

A comprehensive Python library for computational linguistics, text processing,
and language learning for the Mising language of Assam and Arunachal Pradesh.

Author: Mising NLP Project Contributors
License: MIT
"""

__version__ = "0.1.0"
__author__ = "Mising NLP Project Contributors"
__license__ = "MIT"

import sys

# Ensure UTF-8 output across standard streams on Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Unicode & I/O
from mising.unicode_utils import (
    normalize_mising_text,
    detect_script,
    is_mising_character,
    read_mising_file,
    write_mising_file,
    clean_text,
)

# Tokenization
from mising.tokenization import (
    sent_tokenize,
    word_tokenize,
    syllable_tokenize,
    char_tokenize,
    MisingTokenizer,
)

# Morphology & Stemming
from mising.morphology import (
    stem,
    analyze,
    MisingStemmer,
    StemmingMode,
    MisingMorphAnalyzer,
    MorphAnalysis,
    Morpheme,
)

# POS Tagging
from mising.pos import (
    pos_tag,
    MisingPOSTagger,
)

# Transliteration
from mising.transliteration import (
    transliterate,
    mising_to_assamese,
    assamese_to_mising,
    mising_to_ipa,
    mising_to_ascii,
    ascii_to_mising,
    MisingTransliterator,
)

# Corpus
from mising.corpus import (
    CorpusDocument,
    CorpusReader,
    CorpusManager,
    FreqDist,
    compute_ngrams,
    load_sample_corpus,
)

# Language Learning
from mising.learning import (
    THEMATIC_VOCABULARY,
    list_themes,
    get_theme_vocabulary,
    number_to_mising,
    classified_noun,
    CLASSIFIERS_DATA,
    Flashcard,
    FlashcardDeck,
    create_deck,
    DictionaryEntry,
    MisingDictionary,
    get_default_dictionary,
)


def lookup(word: str):
    """Convenience helper to look up a word in the default Mising dictionary."""
    return get_default_dictionary().lookup(word)


__all__ = [
    # Version
    "__version__",
    "__author__",
    "__license__",
    # Unicode & I/O
    "normalize_mising_text",
    "detect_script",
    "is_mising_character",
    "read_mising_file",
    "write_mising_file",
    "clean_text",
    # Tokenization
    "sent_tokenize",
    "word_tokenize",
    "syllable_tokenize",
    "char_tokenize",
    "MisingTokenizer",
    # Morphology
    "stem",
    "analyze",
    "MisingStemmer",
    "StemmingMode",
    "MisingMorphAnalyzer",
    "MorphAnalysis",
    "Morpheme",
    # POS Tagging
    "pos_tag",
    "MisingPOSTagger",
    # Transliteration
    "transliterate",
    "mising_to_assamese",
    "assamese_to_mising",
    "mising_to_ipa",
    "mising_to_ascii",
    "ascii_to_mising",
    "MisingTransliterator",
    # Corpus
    "CorpusDocument",
    "CorpusReader",
    "CorpusManager",
    "FreqDist",
    "compute_ngrams",
    "load_sample_corpus",
    # Learning
    "THEMATIC_VOCABULARY",
    "list_themes",
    "get_theme_vocabulary",
    "number_to_mising",
    "classified_noun",
    "CLASSIFIERS_DATA",
    "Flashcard",
    "FlashcardDeck",
    "create_deck",
    "DictionaryEntry",
    "MisingDictionary",
    "get_default_dictionary",
    "lookup",
]
