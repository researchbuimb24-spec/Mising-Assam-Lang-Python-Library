"""
04_language_learning.py - Vocabulary, Flashcards, Numerals, and Dictionary.
"""

import sys
import mising

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

def main():
    print("=" * 60)
    print("  Mising Language Learning Toolkit")
    print("=" * 60)

    # 1. Thematic Vocabulary
    print("\n1. Thematic Vocabulary Collections:")
    themes = mising.list_themes()
    print(f"   Available Themes: {', '.join(themes)}")
    greetings = mising.get_theme_vocabulary("greetings")
    print(f"   Greetings Sample:")
    for item in greetings[:3]:
        print(f"     • {item['mising']:<15} -> {item['english']:<25} ({item['assamese']})")

    # 2. Numerals and Noun Classifier Generation
    print("\n2. Numerals and Classifier Compounds:")
    numbers_to_test = [1, 2, 5, 10, 15, 20, 23, 100]
    for n in numbers_to_test:
        print(f"   {n:<4} -> {mising.number_to_mising(n)}")

    print("\n   Classified Nouns:")
    print(f"     • 1 person:     {mising.classified_noun('ami', 1)}")
    print(f"     • 2 elephants:  {mising.classified_noun('sine', 2)}")
    print(f"     • 3 houses:     {mising.classified_noun('okum', 3, classifier='pum')}")

    # 3. Flashcards and Anki Deck Export
    print("\n3. Flashcard Decks:")
    deck = mising.create_deck("nature")
    print(f"   Deck Created: '{deck.name}' ({len(deck)} cards)")
    sample_card = deck.cards[0]
    print(f"   Sample Card: Front='{sample_card.front}', Back='{sample_card.back}', IPA=/{sample_card.ipa}/")

    # 4. Interactive Quiz Demonstration
    print("\n4. Multiple Choice Quiz Simulation:")
    quiz = deck.generate_quiz(num_questions=2, seed=42)
    for i, q in enumerate(quiz, 1):
        print(f"\n   Q{i}: What is '{q.prompt}' (/{q.ipa}/, Assamese: {q.assamese})?")
        for opt_idx, opt in enumerate(q.options, 1):
            print(f"       [{opt_idx}] {opt}")
        print(f"       Answer: {q.correct_answer} (verified: {q.check(q.correct_answer)})")

    # 5. Dictionary Lookup
    print("\n5. Dictionary Search:")
    d = mising.get_default_dictionary()
    entry = d.lookup("okum")
    if entry:
        print(f"   Entry: '{entry.mising}' ({entry.pos})")
        print(f"     English:  {entry.english}")
        print(f"     Assamese: {entry.assamese}")
        print(f"     IPA:      /{entry.ipa}/")

    # English reverse lookup
    water_results = d.search_english("water")
    print(f"\n   Reverse search for 'water':")
    for r in water_results:
        print(f"     • {r.mising} ({r.pos}): {r.english}")

if __name__ == "__main__":
    main()
