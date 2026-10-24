"""
Tests for Mising stemming, lemmatization, and morphological analysis.
"""

from mising.morphology import (
    MisingStemmer,
    StemmingMode,
    stem,
    analyze,
    MisingMorphAnalyzer,
)


def test_stem_nominal_case():
    stemmer = MisingStemmer(mode=StemmingMode.LIGHT)
    assert stemmer.stem("okum-lo") == "okum"
    assert stemmer.stem("okumlo") == "okum"
    assert stemmer.stem("dolunglok") == "dolung"
    assert stemmer.stem("amike") == "ami"


def test_stem_nominal_plural():
    stemmer = MisingStemmer(mode=StemmingMode.LIGHT)
    assert stemmer.stem("ami-kídí") == "ami"
    assert stemmer.stem("amikídí") == "ami"
    assert stemmer.stem("amibula") == "ami"


def test_stem_plural_and_case():
    # Plural + case combined: ami-kídí-lo -> ami
    assert stem("ami-kídí-lo") == "ami"
    assert stem("amikídílo") == "ami"


def test_stem_verbal_inflections():
    # Medium mode strips verbal inflections
    stemmer = MisingStemmer(mode=StemmingMode.MEDIUM)
    assert stemmer.stem("gerduŋ") == "ger"
    assert stemmer.stem("gerto") == "ger"
    assert stemmer.stem("gerye") == "ger"
    assert stemmer.stem("gerlang") == "ger"


def test_protect_short_roots():
    # Short roots like 'do' (eat), 'gi' (go), 'ti' (drink) must not be stripped away
    assert stem("doduŋ") == "do"
    assert stem("gito") == "gi"
    assert stem("tiduŋ") == "ti"


def test_aggressive_derivation_stemming():
    # Aggressive mode strips nominalizers like -nam and agentive -ne
    stemmer = MisingStemmer(mode=StemmingMode.AGGRESSIVE)
    assert stemmer.stem("mennam") == "men"
    assert stemmer.stem("ginam") == "gi"
    assert stemmer.stem("gérne") == "gér"


def test_morphological_analyzer():
    res = analyze("ami-kídí-lo")
    assert res.root == "ami"
    assert len(res.morphemes) == 2
    assert res.morphemes[0].gloss == "PL"
    assert res.morphemes[1].gloss == "LOC"
    assert res.features["number"] == "plural"
    assert res.features["case"] == "locative"
    assert res.gloss == "ami-PL-LOC"


def test_morphological_analyzer_verbal():
    res = analyze("ger-duŋ")
    assert res.root == "ger"
    assert res.pos_hint == "VERB"
    assert res.features["aspect"] == "continuous"
    assert res.features["tense"] == "present"
