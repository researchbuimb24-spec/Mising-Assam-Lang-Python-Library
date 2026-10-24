"""
Tests for Part-of-Speech (POS) tagging.
"""

from mising.pos import MisingPOSTagger, pos_tag


def test_pos_tag_basic():
    text = "Ngo okum-lo giduŋ ."
    tagged = pos_tag(text)
    tags_dict = dict(tagged)

    assert tags_dict["Ngo"] == "PRON"
    assert tags_dict["okum-lo"] == "NOUN"
    assert tags_dict["giduŋ"] == "VERB"
    assert tags_dict["."] == "PUNCT"


def test_pos_tag_lexicon_classes():
    tagger = MisingPOSTagger()

    assert tagger.tag_token("ami") == "NOUN"
    assert tagger.tag_token("ger") == "VERB"
    assert tagger.tag_token("kampo") == "ADJ"
    assert tagger.tag_token("ténto") == "ADV"
    assert tagger.tag_token("ako") == "NUM"
    assert tagger.tag_token("oi") == "INTJ"
    assert tagger.tag_token("gí") == "CCONJ"


def test_pos_tag_oov_heuristics():
    tagger = MisingPOSTagger()

    # Verbal continuous suffix -duŋ on unknown root
    assert tagger.tag_token("mosumduŋ") == "VERB"
    # Past suffix -to
    assert tagger.tag_token("mosumto") == "VERB"
    # Plural suffix -kídí on noun
    assert tagger.tag_token("simyo-kídí") == "NOUN"
    # Nominalizer -nam
    assert tagger.tag_token("mosumnam") == "NOUN"


def test_pos_tag_numeral_classifiers():
    tagger = MisingPOSTagger()
    # gor-ako, abor-anyi should tag as NUM
    assert tagger.tag_token("gor-ako") == "NUM"
    assert tagger.tag_token("abor-anyi") == "NUM"


def test_pos_tag_training():
    tagger = MisingPOSTagger()
    sample_corpus = [
        [("XyzWord", "ADJ"), ("okum", "NOUN")],
        [("XyzWord", "ADJ"), ("ami", "NOUN")],
    ]
    tagger.train(sample_corpus)
    assert tagger.tag_token("XyzWord") == "ADJ"
