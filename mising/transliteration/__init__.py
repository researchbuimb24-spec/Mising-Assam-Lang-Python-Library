"""
Transliteration tools for the Mising language.

Provides bidirectional transliteration between:
  - Mising standard Roman orthography (MAK standard)
  - Assamese (Bengali-Assamese) script
  - Simplified ASCII Latin (for easy typing)
  - International Phonetic Alphabet (IPA)
"""

from mising.transliteration.transliterator import (
    MisingTransliterator,
    transliterate,
    mising_to_assamese,
    assamese_to_mising,
    mising_to_ipa,
    mising_to_ascii,
    ascii_to_mising,
)

__all__ = [
    "MisingTransliterator",
    "transliterate",
    "mising_to_assamese",
    "assamese_to_mising",
    "mising_to_ipa",
    "mising_to_ascii",
    "ascii_to_mising",
]
