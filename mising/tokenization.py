"""
Tokenization module for the Mising language.

Provides specialized sentence segmentation, word tokenization, syllable
splitting, and grapheme analysis tailored to Mising orthography (both Latin
MAK orthography and Assamese script).
"""

import re
from typing import List, Optional
from mising.unicode_utils import normalize_mising_text


# Common abbreviations in Mising literature and regional texts to avoid false sentence splits
ABBREVIATIONS = {
    "dr.", "prof.", "mr.", "mrs.", "ms.", "st.", "m.a.k.", "mak.", "a.a.l.",
    "e.g.", "i.e.", "etc.", "no.", "vol.", "p.", "pp."
}

# Regex pattern for sentence boundary detection
# Handles Latin punctuation (. ? !), Indic/Assamese danda (। ॥), and ellipses (...)
_SENTENCE_BOUNDARY_RE = re.compile(
    r'(?<=[.?!।॥])\s+(?=[A-ZÉÍa-z\u0980-\u09FF"\'‘“])'
)

# Word tokenization patterns:
# Matches Mising words with Latin characters, canonical vowels (é, í),
# internal hyphens (for clitics like ami-kídí, ger-duŋ), internal apostrophes/glottal stops,
# Assamese script words, numbers, and standalone punctuation marks.
_WORD_TOKEN_RE = re.compile(
    r"[A-Za-zÉÍéíŋɲ]+(?:(?:[-'][A-Za-zÉÍéíŋɲ]+)+)?"  # Mising Latin words with optional hyphens/apostrophes
    r"|[\u0980-\u09FF]+(?:-[\u0980-\u09FF]+)*"       # Assamese script words
    r"|\d+(?:[.,]\d+)?"                             # Numbers
    r"|[\.\?!।॥,\:;\"'\(\)\[\]\{\}\-—–/\<\>@#$%^&*]" # Punctuation and symbols
)

# Digraphs and compound consonants in Mising
MISING_DIGRAPHS = ["kh", "th", "ph", "ng", "ny", "ch"]
MISING_VOWELS = ["aa", "ee", "ii", "oo", "uu", "éé", "íí", "a", "e", "i", "o", "u", "é", "í"]


def sent_tokenize(text: str) -> List[str]:
    """
    Split Mising text into sentences.

    Supports Latin punctuation (. ? !), Assamese danda (। ॥), and dialogue quotes.
    Correctly ignores abbreviations (such as Dr., MAK., etc.).

    Args:
        text: Input text.

    Returns:
        List of sentence strings.

    Examples:
        >>> text = "Ngo Mising agom kénam ami. No kolo giduŋ? Ngo dolunglo yarto।"
        >>> sent_tokenize(text)
        ['Ngo Mising agom kénam ami.', 'No kolo giduŋ?', 'Ngo dolunglo yarto।']
    """
    if not text or not text.strip():
        return []

    text = normalize_mising_text(text.strip())

    # Protect abbreviations by temporarily replacing their dots
    protected_tokens = {}
    for i, abbr in enumerate(ABBREVIATIONS):
        pattern = re.compile(re.escape(abbr), re.IGNORECASE)
        placeholder = f"__ABBR_{i}__"
        matches = pattern.findall(text)
        if matches:
            protected_tokens[placeholder] = matches[0]
            text = pattern.sub(placeholder, text)

    # Protect decimal numbers (e.g. 3.14)
    def _protect_num(match):
        return match.group(0).replace(".", "__DOT__")

    text = re.sub(r"\d+\.\d+", _protect_num, text)

    # Split using sentence boundary regex
    raw_sentences = _SENTENCE_BOUNDARY_RE.split(text)

    # Secondary split on danda (।) or newlines if any remain unhandled
    sentences = []
    for s in raw_sentences:
        sub_s = re.split(r"(?<=[।॥\n])\s*", s)
        for part in sub_s:
            cleaned = part.strip()
            if cleaned:
                # Restore protected abbreviations and dots
                for placeholder, orig in protected_tokens.items():
                    cleaned = cleaned.replace(placeholder, orig)
                cleaned = cleaned.replace("__DOT__", ".")
                sentences.append(cleaned)

    return sentences


def word_tokenize(
    text: str,
    preserve_hyphenated: bool = True,
    split_clitics: bool = False
) -> List[str]:
    """
    Tokenize Mising text into words and punctuation tokens.

    Mising orthography makes extensive use of hyphens for clitics, plural markers,
    and compounding (e.g. 'ami-kídí' [people], 'ger-duŋ' [is singing], 'ali-aye' [crops]).

    Args:
        text: Input string.
        preserve_hyphenated: If True, keep hyphenated words intact as a single token.
        split_clitics: If True, splits hyphenated clitics into distinct constituent tokens.

    Returns:
        List of token strings.

    Examples:
        >>> word_tokenize("Ngo okum-lo giduŋ.")
        ['Ngo', 'okum-lo', 'giduŋ', '.']
        >>> word_tokenize("Ngo okum-lo giduŋ.", split_clitics=True)
        ['Ngo', 'okum', '-', 'lo', 'giduŋ', '.']
    """
    if not text:
        return []

    text = normalize_mising_text(text)
    tokens = _WORD_TOKEN_RE.findall(text)

    if split_clitics or not preserve_hyphenated:
        result = []
        for tok in tokens:
            if "-" in tok and len(tok) > 1 and not tok.startswith("-"):
                parts = tok.split("-")
                for i, p in enumerate(parts):
                    if p:
                        result.append(p)
                    if i < len(parts) - 1 and split_clitics:
                        result.append("-")
            else:
                result.append(tok)
        return result

    return tokens


def syllable_tokenize(word: str) -> List[str]:
    """
    Split a Mising word into syllables based on Mising phonological structure.

    Mising syllables generally follow (C)V(C) patterns, where V can be a short
    or long vowel ('a', 'aa', 'é', 'éé', etc.) and C can be simple or digraph ('ng', 'ny').

    Args:
        word: A single Mising word (Latin script).

    Returns:
        List of syllable strings.

    Examples:
        >>> syllable_tokenize("doolung")
        ['doo', 'lung']
        >>> syllable_tokenize("kídílo")
        ['kí', 'dí', 'lo']
        >>> syllable_tokenize("apong")
        ['a', 'pong']
    """
    word = word.strip().lower()
    if not word or not word.isalpha():
        return [word] if word else []

    # Recognize vowel centers (including long vowels and canonical diacritics)
    # Sort vowels by length descending to match 'aa' before 'a'
    vowel_pattern = "|".join(sorted(MISING_VOWELS, key=len, reverse=True))
    vowel_matches = list(re.finditer(vowel_pattern, word))

    if not vowel_matches:
        return [word]

    if len(vowel_matches) == 1:
        return [word]

    # Split boundaries between vowel nuclei
    syllables = []
    start = 0

    for i in range(len(vowel_matches) - 1):
        v1_end = vowel_matches[i].end()
        v2_start = vowel_matches[i + 1].start()
        intervocalic = word[v1_end:v2_start]

        # Consonants between vowels:
        # If 0 consonants: hiatus (e.g. a-i, split between them)
        # If 1 consonant: belongs to the next syllable (Onset Maximization)
        # If 2 consonants:
        #   - Check if it's a digraph ('ng', 'ny', 'kh', 'ph', 'th'): belongs to onset of next
        #   - Otherwise, split between coda and onset (e.g. ok-um, ger-to)
        if len(intervocalic) == 0:
            split_idx = v1_end
        elif len(intervocalic) == 1:
            split_idx = v1_end
        else:
            if intervocalic in MISING_DIGRAPHS:
                split_idx = v1_end
            elif any(intervocalic.endswith(dg) for dg in MISING_DIGRAPHS):
                # e.g., 'mp' or 'rny'
                split_idx = v1_end + (len(intervocalic) - 2)
            else:
                # Divide consonants between syllables
                split_idx = v1_end + 1

        syllables.append(word[start:split_idx])
        start = split_idx

    syllables.append(word[start:])
    return [s for s in syllables if s]


def char_tokenize(text: str, group_digraphs: bool = True) -> List[str]:
    """
    Tokenize text into characters or phonological graphemes.

    When `group_digraphs=True`, character digraphs like 'ng', 'ny', 'kh', 'th', 'ph'
    and long vowels 'aa', 'ee', etc., are kept as single phonetic grapheme units.

    Args:
        text: Input string.
        group_digraphs: Whether to preserve standard Mising digraphs as single tokens.

    Returns:
        List of grapheme tokens.

    Examples:
        >>> char_tokenize("apong", group_digraphs=True)
        ['a', 'p', 'o', 'ng']
        >>> char_tokenize("apong", group_digraphs=False)
        ['a', 'p', 'o', 'n', 'g']
    """
    if not text:
        return []

    text = normalize_mising_text(text)
    if not group_digraphs:
        return list(text)

    # Regex matching digraphs and long vowels first, then single characters
    units = sorted(MISING_VOWELS + MISING_DIGRAPHS, key=len, reverse=True)
    pattern = re.compile("|".join(re.escape(u) for u in units), re.IGNORECASE)

    result = []
    i = 0
    n = len(text)
    while i < n:
        match = pattern.match(text, i)
        if match:
            result.append(match.group(0))
            i = match.end()
        else:
            result.append(text[i])
            i += 1

    return result


class MisingTokenizer:
    """
    Configurable tokenizer instance for Mising text processing pipelines.
    """

    def __init__(self, preserve_hyphenated: bool = True, split_clitics: bool = False):
        self.preserve_hyphenated = preserve_hyphenated
        self.split_clitics = split_clitics

    def tokenize_sentences(self, text: str) -> List[str]:
        return sent_tokenize(text)

    def tokenize_words(self, text: str) -> List[str]:
        return word_tokenize(
            text,
            preserve_hyphenated=self.preserve_hyphenated,
            split_clitics=self.split_clitics,
        )

    def tokenize_syllables(self, word: str) -> List[str]:
        return syllable_tokenize(word)

    def tokenize(self, text: str) -> List[List[str]]:
        """
        Tokenize into a nested list of sentences and words.
        """
        sentences = self.tokenize_sentences(text)
        return [self.tokenize_words(s) for s in sentences]
