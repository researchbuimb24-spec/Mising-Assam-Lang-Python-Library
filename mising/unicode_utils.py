"""
Unicode utilities and text normalization for the Mising language.

Mising (ISO 639-3: mhu), a member of the Tani branch of the Sino-Tibetan
language family spoken in Assam and Arunachal Pradesh, is officially written in
a modified Latin orthography standardized by the Mising Agom Kébang (MAK).
It is also written or transcribed in the Assamese (Bengali-Assamese) script.

This module provides robust Unicode handling, normalization, script detection,
file I/O, and character classification for both orthographic conventions.
"""

import unicodedata
from pathlib import Path
from typing import Dict, List, Set, Union

# --- Character Sets for Mising Latin Orthography (MAK Standard) ---

# Vowel inventory:
# Short vowels: a, e, i, o, u, é (/ə/), í (/ɨ/)
VOWELS_SHORT_LOWER: Set[str] = {"a", "e", "i", "o", "u", "é", "í"}
VOWELS_SHORT_UPPER: Set[str] = {"A", "E", "I", "O", "U", "É", "Í"}
VOWELS_SHORT: Set[str] = VOWELS_SHORT_LOWER | VOWELS_SHORT_UPPER

# Long vowels in MAK orthography are typically written as doubled vowels:
# aa, ee, ii, oo, uu, éé, íí (or occasionally with macron: ā, ē, ī, ō, ū)
VOWELS_LONG_LOWER: Set[str] = {"aa", "ee", "ii", "oo", "uu", "éé", "íí"}
VOWELS_ALL_LOWER: Set[str] = VOWELS_SHORT_LOWER | VOWELS_LONG_LOWER

# Consonant inventory:
# Stops/Affricates: p, ph, b, t, th, d, c, j, k, kh, g
# Nasals: m, n, ny (/ɲ/), ng (/ŋ/)
# Fricatives: s, h
# Liquids/Glides: r, l, y, w
CONSONANTS_SINGLE_LOWER: Set[str] = {
    "k", "g", "c", "j", "t", "d", "n", "p", "b", "m", "y", "r", "l", "s", "h", "w"
}
CONSONANT_DIGRAPHS_LOWER: List[str] = ["kh", "th", "ph", "ng", "ny"]

# Assamese script Unicode blocks: U+0980 to U+09FF
ASSAMESE_UNICODE_RANGE = (0x0980, 0x09FF)

# Mising diacritic variants mapped to MAK canonical form:
# e.g. acute accent variations, schwa, barred-i, circumflex
VOWEL_CANONICAL_MAP: Dict[str, str] = {
    # Variations for 'é' (/ə/ - mid-central unrounded)
    "e\u0301": "é",   # e + combining acute
    "E\u0301": "É",   # E + combining acute
    "è": "é",         # grave sometimes typed
    "È": "É",
    "ë": "é",         # diaeresis variant
    "Ë": "É",
    "ə": "é",         # IPA schwa
    "Ə": "É",
    # Variations for 'í' (/ɨ/ - high-central unrounded)
    "i\u0301": "í",   # i + combining acute
    "I\u0301": "Í",   # I + combining acute
    "ì": "í",
    "Ì": "Í",
    "ï": "í",         # diaeresis variant
    "Ï": "Í",
    "ɨ": "í",         # IPA barred i
    "Ɨ": "Í",
    # Macro variants to doubled vowels if preferred
    "ā": "aa", "Ā": "Aa",
    "ē": "ee", "Ē": "Ee",
    "ī": "ii", "Ī": "Ii",
    "ō": "oo", "Ō": "Oo",
    "ū": "uu", "Ū": "Uu",
}

# Standardized quotation and punctuation normalization
PUNCTUATION_NORMALIZATION: Dict[str, str] = {
    "‘": "'",
    "’": "'",
    "“": '"',
    "”": '"',
    "–": "-",
    "—": "-",
    "…": "...",
    " ।": "।",
    " ॥": "॥",
}


def normalize_mising_text(text: str, canonical_vowels: bool = True) -> str:
    """
    Normalize Mising text to Unicode NFC and canonical MAK orthography.

    Args:
        text: The raw input string in Mising (Latin or Assamese script).
        canonical_vowels: Whether to normalize diacritic variations (like
            combining accents, schwa, barred i) to the official MAK vowels ('é', 'í').

    Returns:
        A cleanly normalized Unicode string.

    Examples:
        >>> normalize_mising_text("ami-kídí-lo")
        'ami-kídí-lo'
        >>> normalize_mising_text("ami-ki\u0301di\u0301-lo")
        'ami-kídí-lo'
        >>> normalize_mising_text("gerduŋ ‘Mising’")
        'gerduŋ \\'Mising\\''
    """
    if not text:
        return ""

    # 1. Unicode NFC normalization (composes characters like e + acute into precomposed é)
    text = unicodedata.normalize("NFC", text)

    # 2. Canonical vowel mappings (handle legacy or alternative representations)
    if canonical_vowels:
        for variant, canonical in VOWEL_CANONICAL_MAP.items():
            if variant in text:
                text = text.replace(variant, canonical)

    # 3. Standardize quotes, dashes, and whitespace
    for original, replacement in PUNCTUATION_NORMALIZATION.items():
        if original in text:
            text = text.replace(original, replacement)

    # 4. Remove invisible zero-width spaces/joiners if stray
    text = text.replace("\u200b", "").replace("\ufeff", "")

    return text


def detect_script(text: str) -> str:
    """
    Detect the predominant script used in the given text.

    Returns:
        One of 'latin', 'assamese', 'mixed', or 'unknown'.

    Examples:
        >>> detect_script("Ngo Mising agom kénam ami.")
        'latin'
        >>> detect_script("ঙম মিচিং আগম কীনাম অমি।")
        'assamese'
    """
    latin_count = 0
    assamese_count = 0

    for ch in text:
        code = ord(ch)
        if ASSAMESE_UNICODE_RANGE[0] <= code <= ASSAMESE_UNICODE_RANGE[1]:
            assamese_count += 1
        elif ch.isalpha() and ("LATIN" in unicodedata.name(ch, "")):
            latin_count += 1

    total = latin_count + assamese_count
    if total == 0:
        return "unknown"

    latin_ratio = latin_count / total
    assamese_ratio = assamese_count / total

    if latin_ratio > 0.85:
        return "latin"
    if assamese_ratio > 0.85:
        return "assamese"
    return "mixed"


def is_mising_character(char: str) -> bool:
    """
    Check if a character is part of the standard Mising Latin alphabet.

    Args:
        char: Single character string.

    Returns:
        True if the character is a recognized Mising Latin letter.
    """
    if len(char) != 1:
        return False
    lower = char.lower()
    return (
        lower in VOWELS_SHORT_LOWER
        or lower in CONSONANTS_SINGLE_LOWER
        or lower in {"ŋ", "ɲ"}
    )


def clean_text(text: str) -> str:
    """
    Clean extra spaces, newlines, and trailing punctuation while preserving
    structural paragraph boundaries.
    """
    text = normalize_mising_text(text)
    lines = [line.strip() for line in text.splitlines()]
    cleaned_lines = [line for line in lines if line]
    return "\n".join(cleaned_lines)


def read_mising_file(filepath: Union[str, Path], encoding: str = "utf-8", normalize: bool = True) -> str:
    """
    Read a text file containing Mising text with robust Unicode handling.

    Args:
        filepath: Path to the text file.
        encoding: File encoding (defaults to 'utf-8').
        normalize: Whether to automatically normalize text upon reading.

    Returns:
        The content of the file as a string.
    """
    path = Path(filepath)
    with path.open("r", encoding=encoding, errors="replace") as f:
        content = f.read()
    if normalize:
        return normalize_mising_text(content)
    return content


def write_mising_file(
    filepath: Union[str, Path],
    text: str,
    encoding: str = "utf-8",
    normalize: bool = True
) -> None:
    """
    Write Mising text to a file using UTF-8 encoding.

    Args:
        filepath: Destination file path.
        text: String content to write.
        encoding: File encoding (defaults to 'utf-8').
        normalize: Whether to normalize text before writing.
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    if normalize:
        text = normalize_mising_text(text)
    with path.open("w", encoding=encoding) as f:
        f.write(text)
