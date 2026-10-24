# Mising NLP (মিচিং / Mising Agom Toolkit)

[![Python Versions](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/tests-53%20passed-brightgreen.svg)]()
[![Code Style: Clean](https://img.shields.io/badge/code%20style-pep8-green.svg)]()

A comprehensive, modular Python library for Natural Language Processing (NLP), computational linguistics, digital preservation, and language learning for the **Mising language** (*Mising Agom*), spoken by the indigenous Mising community in Assam and Arunachal Pradesh, India.

---

## Table of Contents

- [About the Mising Language](#about-the-mising-language)
- [Key Features](#key-features)
- [Installation](#installation)
- [Quick Start Guide](#quick-start-guide)
  - [1. Unicode Support & Normalization](#1-unicode-support--normalization)
  - [2. Tokenization](#2-tokenization)
  - [3. Morphological Analysis & Stemming](#3-morphological-analysis--stemming)
  - [4. Part-of-Speech Tagging](#4-part-of-speech-tagging)
  - [5. Multi-Script Transliteration](#5-multi-script-transliteration)
  - [6. Corpus Management & Linguistic Search](#6-corpus-management--linguistic-search)
  - [7. Language Learning Helpers](#7-language-learning-helpers)
- [Command-Line Interface (CLI)](#command-line-interface-cli)
- [Architecture & Design](#architecture--design)
- [Testing](#testing)
- [Contributing & Digital Preservation](#contributing--digital-preservation)
- [License](#license)

---

## About the Mising Language

The **Mising** (also *Mishing*, *Plains Miri*, ISO 639-3: `mhu`) language belongs to the **Tani branch** of the **Sino-Tibetan** family. It is spoken by over 600,000 people primarily in the Brahmaputra valley districts of Assam (Dhemaji, Lakhimpur, Majuli, Sonitpur, Biswanath, Golaghat, Jorhat, Sivasagar, Dibrugarh, Tinsukia) and East Siang in Arunachal Pradesh.

### Orthographic Conventions:
- **Standard Roman Orthography**: Formally standardized by the **Mising Agom Kébang (MAK)** in 1972. It features standard Latin characters plus two crucial central vowels:
  - `é`: represents the mid-central unrounded vowel /ə/ (schwa).
  - `í`: represents the high-central unrounded vowel /ɨ/.
  - Long vowels are indicated by doubling: `aa`, `ee`, `ii`, `oo`, `uu`, `éé`, `íí`.
  - Digraph consonants include `ng` (/ŋ/) and `ny` (/ɲ/).
- **Assamese Script (অসমীয়া লিপি)**: Historically and contemporarily used in regional bilingual publications, where specific diacritics represent Mising vowels (e.g. `এ'` for `é`, `ই'` for `í`).

### Morphological Structure:
Mising is an **agglutinative language** with extensive suffixation:
- **Nouns**: Stem + Plural Marker (`-kídí`, `-bula`) + Case Marker (`-lo` [Locative], `-lok` [Ablative], `-ke` [Genitive], `-m`/`-am` [Accusative], `-e` [Ergative]).
- **Verbs**: Root + Aspect/Tense (`-duŋ` [Continuous], `-to` [Past], `-ka` [Perfect], `-ye` [Future]) + Mood/Imperative (`-lang`) + Negation (`-ma`, `-mang`) or Nominalizer (`-nam`).
- **Numeral Classifiers**: Counting requires obligatory classifiers (e.g., `gor` for humans: *ami gor-ako*, `abor` for animals: *sine abor-anyi*, `pum` for houses: *okum pum-aum*).

---

## Key Features

- **Unicode & Normalization**: Canonical Unicode NFC normalization, combining character unification, diacritic repair, script detection, and UTF-8 file I/O.
- **Linguistic Tokenization**: Sentence segmentation supporting Latin and Assamese punctuation (`.`, `?`, `!`, `।`, `॥`), hyphenated clitic preservation, syllable segmentation, and grapheme extraction.
- **Morphological Analysis**: Configurable stemmer (`LIGHT`, `MEDIUM`, `AGGRESSIVE`) and Leipzig-style interlinear morpheme glossing (`ami-kídí-lo` -> `ami[NOUN] + -kídí[PL] + -lo[LOC]`).
- **Part-of-Speech Tagging**: Universal Dependencies (UD) tagset tagger with built-in lexicon, morphological affix heuristics, and custom corpus training capabilities.
- **Multi-Script Transliteration**: Bidirectional transliteration between Mising MAK Roman, Assamese script, International Phonetic Alphabet (IPA), and ASCII.
- **Corpus Management & Search**: Concordance (KWIC) search, regex matching, vocabulary frequency distributions (`FreqDist`), N-gram generator, and authentic cultural sample texts (*Ali-Aye-Ligang*, *Do:ying* proverbs, folktales).
- **Language Learning Toolkit**: Thematic vocabulary decks (greetings, kinship, nature, body parts, animals), numeral word generator with classifiers, Anki flashcard exporter, interactive multiple-choice quizzes, and a trilingual dictionary (Mising - English - Assamese).
- **Zero Heavy Dependencies**: Pure Python implementation with zero mandatory external packages, running seamlessly on Python 3.7 through 3.12+.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/mising-nlp/mising.git
cd mising

# Install in editable mode
pip install -e .

# Or install with developer dependencies (pytest)
pip install -e ".[dev]"
```

---

## Quick Start Guide

### 1. Unicode Support & Normalization

```python
import mising

# Normalize text with combining diacritics or non-standard characters
raw = "ami-ki\u0301di\u0301-lo ‘Mising’ agom"
normalized = mising.normalize_mising_text(raw)
print(normalized)  # Output: ami-kídí-lo 'Mising' agom

# Detect script
print(mising.detect_script("Ngo Mising agom kénam ami."))  # Output: latin
print(mising.detect_script("ঙম মিচিং আগম কীনাম অমি।"))      # Output: assamese
```

### 2. Tokenization

```python
import mising

text = "Ngo Mising agom kénam ami. No kolo giduŋ? Ngo okum-lo yarto।"

# Sentence segmentation
sentences = mising.sent_tokenize(text)
print(sentences)
# ['Ngo Mising agom kénam ami.', 'No kolo giduŋ?', 'Ngo okum-lo yarto।']

# Word tokenization (preserves clitics and compounds by default)
tokens = mising.word_tokenize("Ngo okum-lo giduŋ.")
print(tokens)
# ['Ngo', 'okum-lo', 'giduŋ', '.']

# Syllable segmentation
print(mising.syllable_tokenize("doolung"))  # ['doo', 'lung']
print(mising.syllable_tokenize("apong"))    # ['a', 'pong']
```

### 3. Morphological Analysis & Stemming

```python
import mising

# Stemming
print(mising.stem("ami-kídí-lo"))  # Output: ami
print(mising.stem("gerduŋ"))       # Output: ger
print(mising.stem("okum-lo"))      # Output: okum
print(mising.stem("mennam", mode=mising.StemmingMode.AGGRESSIVE))  # Output: men

# Interlinear Morphological Analysis
analysis = mising.analyze("ami-kídí-lo")
print(analysis.root)     # 'ami'
print(analysis.gloss)    # 'ami-PL-LOC'
print(analysis.features) # {'number': 'plural', 'case': 'locative'}
print(analysis.summary())
```

### 4. Part-of-Speech Tagging

```python
import mising

text = "Ngo okum-lo giduŋ ."
tagged = mising.pos_tag(text)
print(tagged)
# [('Ngo', 'PRON'), ('okum-lo', 'NOUN'), ('giduŋ', 'VERB'), ('.', 'PUNCT')]
```

### 5. Multi-Script Transliteration

```python
import mising

# Roman to Assamese Script
as_text = mising.mising_to_assamese("Mising agom")
print(as_text)  # Output: মিচিং আগম্ / মিসিং আগম্

# Roman to IPA Phonetic Transcription
ipa = mising.mising_to_ipa("apong")
print(ipa)  # Output: apoŋ

# ASCII Keyboard Input to Canonical Diacritics
diacritics = mising.ascii_to_mising("ami-ki'di'-lo")
print(diacritics)  # Output: ami-kídí-lo
```

### 6. Corpus Management & Linguistic Search

```python
import mising

# Load built-in authenticated sample corpus
corpus = mising.load_sample_corpus()

# Corpus Statistics
print(corpus.stats())
# {'document_count': 4, 'sentence_count': 21, 'total_tokens': 168, 'unique_words': 105, ...}

# Key Word In Context (KWIC) / Concordance Search
matches = corpus.concordance("agom", window=4)
for m in matches:
    print(m.format())

# Frequency Distribution & Vocabulary
vocab = corpus.vocabulary()
print(vocab.ascii_chart(top_n=5))

# N-grams (Bigrams)
bigrams = corpus.ngrams(n=2)
print(bigrams.most_common(3))
```

### 7. Language Learning Helpers

```python
import mising

# Number generation (cardinal words)
print(mising.number_to_mising(15))  # 'iing-ango'
print(mising.number_to_mising(23))  # 'nyiing-aum'

# Classifier compounds
print(mising.classified_noun("ami", 1))                 # 'ami gor-ako' (1 person)
print(mising.classified_noun("sine", 2))                # 'sine abor-anyi' (2 elephants)
print(mising.classified_noun("okum", 3, classifier="pum")) # 'okum pum-aum' (3 houses)

# Flashcard Deck & Anki Export
deck = mising.create_deck("greetings")
deck.export_anki_csv("mising_greetings_anki.csv")

# Generate interactive multiple-choice quiz
quiz = deck.generate_quiz(num_questions=3)
for q in quiz:
    print(q.prompt, q.options)

# Trilingual Dictionary Lookup
entry = mising.lookup("okum")
print(entry.english)   # 'house, home, dwelling'
print(entry.assamese)  # 'ঘৰ, গৃহ'
```

---

## Command-Line Interface (CLI)

The library provides a CLI tool accessible as `mising` or `python -m mising`:

```bash
# Tokenization
mising tokenize "Ngo Mising agom kénam ami. No inlang!"

# POS Tagging
mising tag "Ngo okum-lo giduŋ."

# Morphological Analysis & Stemming
mising analyze "ger-duŋ-ma"
mising stem "ami-kídí-lo"

# Transliteration
mising transliterate "Mising agom" --target assamese
mising transliterate "apong" --target ipa

# Number & Classified Noun Generator
mising number 15 --noun ami

# Dictionary Search
mising dict "okum"
mising dict "water"

# Corpus Statistics
mising corpus stats
mising corpus concordance "agom"

# Interactive Quiz Mode
mising quiz --theme greetings --count 5
```

---

## Architecture & Design

The library is organized into clear, focused modules adhering to single-responsibility and extensible software principles:

```
assamese_pylib/
├── LICENSE                 # MIT License
├── README.md               # Documentation
├── pyproject.toml          # PEP 517 / 621 packaging
├── setup.py                # Setuptools configuration
├── mising/                 # Core package
│   ├── __init__.py         # High-level clean public API
│   ├── __main__.py         # CLI module execution entrypoint
│   ├── cli.py              # Command-line interface
│   ├── unicode_utils.py    # Unicode normalization, NFC, character sets, I/O
│   ├── tokenization.py     # Sentence, word, syllable, and grapheme tokenizers
│   ├── morphology/         # Morphological analysis & lemmatization
│   │   ├── stemmer.py      # Rule-based agglutinative stemmer
│   │   └── analyzer.py     # Interlinear morpheme glossing (Leipzig standard)
│   ├── pos/                # Part-of-Speech tagging
│   │   └── tagger.py       # Universal POS tagger & heuristics
│   ├── transliteration/    # Multi-script conversion
│   │   └── transliterator.py# Roman <-> Assamese <-> IPA <-> ASCII engine
│   ├── corpus/             # Text collection management
│   │   ├── reader.py       # Document loaders (TXT, JSONL, CSV)
│   │   ├── manager.py      # Concordance (KWIC), regex search, indexer
│   │   ├── stats.py        # FreqDist, TTR, N-grams, ASCII chart
│   │   └── sample_data.py  # Authentic Mising cultural texts
│   └── learning/           # Language pedagogy
│       ├── vocabulary.py   # Thematic wordlists with IPA & Assamese
│       ├── numbers.py      # Numeral grammar & classifier synthesis
│       ├── flashcards.py   # Flashcards, Anki exporter, quiz generator
│       └── dictionary.py   # Trilingual dictionary (Mising-English-Assamese)
├── tests/                  # Test suite (53 tests, 100% pass)
└── examples/               # Demonstrative runnable scripts
    ├── 01_quickstart.py
    ├── 02_transliteration_demo.py
    ├── 03_corpus_analysis.py
    └── 04_language_learning.py
```

---

## Testing

Run the test suite using `pytest`:

```bash
pytest -v
```

All 53 unit tests cover every component including Unicode edge cases, agglutinative suffix stripping, POS tagging, script roundtripping, corpus searches, and CLI execution.

---

## Contributing & Digital Preservation

The Mising language represents a rich linguistic and cultural heritage of Assam and the Northeast of India. This library aims to empower researchers, educators, and language technologists to build digital tools, spellcheckers, educational apps, and machine learning models for low-resource languages.

Contributions are warmly welcomed! Please open an issue or pull request to add:
- Expanded vocabulary and dictionary entries
- Additional dialectal annotations
- Curated open corpora

---

## License

This project is licensed under the [MIT License](LICENSE).
