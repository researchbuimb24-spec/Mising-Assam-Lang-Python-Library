"""
Tests for language learning helpers (vocabulary, numbers, flashcards, dictionary).
"""

from mising.learning import (
    THEMATIC_VOCABULARY,
    list_themes,
    get_theme_vocabulary,
    number_to_mising,
    classified_noun,
    Flashcard,
    FlashcardDeck,
    create_deck,
    MisingDictionary,
    get_default_dictionary,
)


def test_thematic_vocabulary():
    themes = list_themes()
    assert "greetings" in themes
    assert "family" in themes
    assert "animals" in themes

    greetings = get_theme_vocabulary("greetings")
    assert len(greetings) > 0
    words = [item["mising"] for item in greetings]
    assert "Kuye" in words


def test_numbers_to_mising():
    assert number_to_mising(1) == "ako"
    assert number_to_mising(2) == "anyi"
    assert number_to_mising(10) == "iing"
    assert number_to_mising(15) == "iing-ango"
    assert number_to_mising(20) == "nyiing"
    assert number_to_mising(23) == "nyiing-aum"
    assert number_to_mising(100) == "lingko"


def test_classified_nouns():
    # Human classifier 'gor'
    phrase1 = classified_noun("ami", 1)
    assert phrase1 == "ami gor-ako"

    # Animal classifier 'abor'
    phrase2 = classified_noun("sine", 2)
    assert phrase2 == "sine abor-anyi"

    # Explicit override
    phrase3 = classified_noun("okum", 3, classifier="pum")
    assert phrase3 == "okum pum-aum"


def test_flashcards_and_deck():
    deck = create_deck("greetings")
    assert len(deck) > 0
    card = deck.cards[0]
    assert isinstance(card, Flashcard)
    assert card.front
    assert card.back


def test_quiz_generation():
    deck = create_deck("animals")
    quiz = deck.generate_quiz(num_questions=3, seed=42)
    assert len(quiz) == 3
    q = quiz[0]
    assert len(q.options) == 4
    assert q.correct_answer in q.options
    assert q.check(q.correct_answer) is True
    assert q.check("definitely_wrong_answer_xyz") is False


def test_dictionary_lookups():
    d = get_default_dictionary()
    entry = d.lookup("okum")
    assert entry is not None
    assert entry.pos == "NOUN"
    assert "house" in entry.english.lower()

    # Search english keyword
    results = d.search_english("water")
    assert len(results) >= 1
    assert any(e.mising == "asi" for e in results)

    # Prefix search
    prefix_results = d.prefix_search("do")
    assert any(e.mising == "do" for e in prefix_results)
    assert any(e.mising == "doolung" for e in prefix_results)
