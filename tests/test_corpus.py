"""
Tests for Corpus management, search, and statistical metrics.
"""

from mising.corpus import (
    CorpusDocument,
    CorpusManager,
    FreqDist,
    compute_ngrams,
    load_sample_corpus,
)


def test_corpus_document_properties():
    doc = CorpusDocument(
        id="doc1",
        title="Test Document",
        text="Ngo Mising agom kénam ami. No inlang!",
        metadata={"author": "Test Author"},
    )
    assert doc.sentence_count == 2
    assert doc.word_count > 0
    assert "Mising" in doc.tokens


def test_corpus_manager_search():
    corpus = CorpusManager()
    corpus.add_text("Ngo Mising agom kénam ami.", title="Doc 1", doc_id="d1")
    corpus.add_text("No Mising agomlo gerlang.", title="Doc 2", doc_id="d2")

    # Concordance search for 'agom'
    conc = corpus.concordance("agom")
    assert len(conc) >= 1
    assert any(c.match.lower() == "agom" for c in conc)


def test_corpus_manager_regex_search():
    corpus = CorpusManager()
    corpus.add_text("Ngo doolunglo giduŋ.", title="Doc 1", doc_id="d1")
    corpus.add_text("Bi okumlo yarto.", title="Doc 2", doc_id="d2")

    # Search for words ending with -duŋ (present continuous)
    matches = corpus.search_regex(r"\w+duŋ")
    assert len(matches) == 1
    assert "giduŋ" in matches[0][2]


def test_freq_dist_and_stats():
    tokens = ["ngo", "mising", "agom", "mising", "ami"]
    fdist = FreqDist(tokens)

    assert fdist["mising"] == 2
    assert fdist["ngo"] == 1
    assert fdist.total_tokens == 5
    assert fdist.unique_types == 4
    assert fdist.type_token_ratio == 0.8
    assert len(fdist.hapaxes()) == 3


def test_compute_ngrams():
    tokens = ["ngo", "mising", "agom", "kénam"]
    bigrams = compute_ngrams(tokens, n=2)
    assert len(bigrams) == 3
    assert bigrams[0] == ("ngo", "mising")
    assert bigrams[1] == ("mising", "agom")


def test_sample_corpus():
    corpus = load_sample_corpus()
    assert len(corpus) >= 4
    stats = corpus.stats()
    assert stats["total_tokens"] > 50
    assert stats["unique_words"] > 20
    assert stats["type_token_ratio"] > 0
