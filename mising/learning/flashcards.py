"""
Interactive flashcards and quiz generator for Mising language learners.
"""

import csv
import json
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from mising.learning.vocabulary import THEMATIC_VOCABULARY


@dataclass
class Flashcard:
    """Represents a single flashcard."""
    front: str            # Mising word / phrase
    back: str             # English definition
    assamese: str         # Assamese script translation
    ipa: str              # IPA phonetic transcription
    category: str         # Theme / Category
    example: str = ""     # Example sentence
    example_translation: str = ""

    def to_dict(self) -> Dict[str, str]:
        return {
            "front": self.front,
            "back": self.back,
            "assamese": self.assamese,
            "ipa": self.ipa,
            "category": self.category,
            "example": self.example,
            "example_translation": self.example_translation,
        }


@dataclass
class QuizQuestion:
    """Represents a multiple-choice quiz question."""
    prompt: str
    correct_answer: str
    options: List[str]
    ipa: str
    assamese: str
    category: str

    def check(self, chosen_option: str) -> bool:
        """Verify if user answer matches the correct choice."""
        return chosen_option.strip().lower() == self.correct_answer.strip().lower()


class FlashcardDeck:
    """
    Collection of flashcards with quiz generation and Anki/CSV export capabilities.
    """

    def __init__(self, name: str = "Mising Language Deck", cards: Optional[List[Flashcard]] = None):
        self.name = name
        self.cards: List[Flashcard] = cards or []

    def add_card(self, card: Flashcard) -> None:
        self.cards.append(card)

    def __len__(self) -> int:
        return len(self.cards)

    def shuffle(self) -> None:
        """Shuffle the deck in-place."""
        random.shuffle(self.cards)

    def export_anki_csv(self, filepath: Union[str, Path]) -> None:
        """
        Export flashcards to a CSV format ready for direct import into Anki.

        Format: Front (Mising), Back (English), IPA, Assamese, Tags
        """
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            for card in self.cards:
                front_field = f"<b>{card.front}</b><br><small>/{card.ipa}/</small>"
                back_field = f"{card.back}<br><small>({card.assamese})</small>"
                if card.example:
                    back_field += f"<br><i>Example: {card.example}</i>"
                writer.writerow([front_field, back_field, card.ipa, card.assamese, card.category])

    def export_json(self, filepath: Union[str, Path]) -> None:
        """Export deck to JSON."""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "name": self.name,
            "count": len(self.cards),
            "cards": [c.to_dict() for c in self.cards],
        }
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def generate_quiz(self, num_questions: int = 5, seed: Optional[int] = None) -> List[QuizQuestion]:
        """
        Generate multiple-choice quiz questions with plausible distractors.

        Args:
            num_questions: Number of questions to generate.
            seed: Optional random seed for reproducible quizzes.

        Returns:
            List of QuizQuestion objects.
        """
        if not self.cards:
            return []

        rng = random.Random(seed)
        count = min(num_questions, len(self.cards))
        selected_cards = rng.sample(self.cards, count)
        all_meanings = [c.back for c in self.cards]

        quiz: List[QuizQuestion] = []
        for card in selected_cards:
            correct = card.back
            # Pick 3 random distractors from other cards
            other_meanings = [m for m in all_meanings if m != correct]
            distractors = rng.sample(other_meanings, min(3, len(other_meanings)))
            options = [correct] + distractors
            rng.shuffle(options)

            quiz.append(
                QuizQuestion(
                    prompt=card.front,
                    correct_answer=correct,
                    options=options,
                    ipa=card.ipa,
                    assamese=card.assamese,
                    category=card.category,
                )
            )

        return quiz


def create_deck(theme: Optional[str] = None) -> FlashcardDeck:
    """
    Create a pre-populated flashcard deck from thematic vocabulary.

    Args:
        theme: Optional specific theme (e.g. 'greetings', 'nature'). If None, loads all themes.

    Returns:
        A ready-to-use FlashcardDeck.

    Examples:
        >>> deck = create_deck("greetings")
        >>> len(deck) > 0
        True
    """
    cards: List[Flashcard] = []
    themes = [theme] if theme else THEMATIC_VOCABULARY.keys()

    for th in themes:
        items = THEMATIC_VOCABULARY.get(th.lower(), [])
        for item in items:
            cards.append(
                Flashcard(
                    front=item["mising"],
                    back=item["english"],
                    assamese=item["assamese"],
                    ipa=item["ipa"],
                    category=th,
                )
            )

    deck_name = f"Mising {theme.title() if theme else 'All'} Vocabulary"
    return FlashcardDeck(name=deck_name, cards=cards)
