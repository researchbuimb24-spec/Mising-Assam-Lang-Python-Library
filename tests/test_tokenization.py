"""
Tests for sentence, word, syllable, and character tokenization.
"""

from mising.tokenization import (
    sent_tokenize,
    word_tokenize,
    syllable_tokenize,
    char_tokenize,
    MisingTokenizer,
)


def test_sent_tokenize_basic():
    text = "Ngo Mising agom kénam ami. No kolo giduŋ? Ngo dolunglo yarto!"
    sents = sent_tokenize(text)
    assert len(sents) == 3
    assert sents[0] == "Ngo Mising agom kénam ami."
    assert sents[1] == "No kolo giduŋ?"
    assert sents[2] == "Ngo dolunglo yarto!"


def test_sent_tokenize_with_assamese_danda():
    text = "ঙম মিচিং আগম কীনাম অমি। ন কল গিদুং?"
    sents = sent_tokenize(text)
    assert len(sents) == 2
    assert sents[0] == "ঙম মিচিং আগম কীনাম অমি।"
    assert sents[1] == "ন কল গিদুং?"


def test_sent_tokenize_abbreviations():
    text = "Dr. Pegu M.A.K. kídíke kebanglo inlang. Bi botte ami."
    sents = sent_tokenize(text)
    assert len(sents) == 2
    assert "Dr. Pegu" in sents[0]


def test_word_tokenize_basic():
    text = "Ngo okum-lo giduŋ."
    tokens = word_tokenize(text)
    assert tokens == ["Ngo", "okum-lo", "giduŋ", "."]


def test_word_tokenize_preserve_clitics():
    text = "ami-kídí-lo ger-duŋ-ma"
    # When preserving clitics
    tokens_preserved = word_tokenize(text, preserve_hyphenated=True)
    assert tokens_preserved == ["ami-kídí-lo", "ger-duŋ-ma"]

    # When splitting clitics
    tokens_split = word_tokenize(text, preserve_hyphenated=False, split_clitics=True)
    assert tokens_split == ["ami", "-", "kídí", "-", "lo", "ger", "-", "duŋ", "-", "ma"]


def test_syllable_tokenize():
    # Single syllables and multisyllabic words
    assert syllable_tokenize("apong") == ["a", "pong"]
    assert syllable_tokenize("doolung") == ["doo", "lung"]
    assert syllable_tokenize("kídí") == ["kí", "dí"]
    assert syllable_tokenize("ami") == ["a", "mi"]


def test_char_tokenize_digraphs():
    text = "apong"
    grouped = char_tokenize(text, group_digraphs=True)
    assert grouped == ["a", "p", "o", "ng"]

    ungrouped = char_tokenize(text, group_digraphs=False)
    assert ungrouped == ["a", "p", "o", "n", "g"]


def test_tokenizer_class():
    tokenizer = MisingTokenizer(preserve_hyphenated=True)
    text = "Ngo giduŋ. No inlang."
    nested = tokenizer.tokenize(text)
    assert len(nested) == 2
    assert nested[0] == ["Ngo", "giduŋ", "."]
    assert nested[1] == ["No", "inlang", "."]
