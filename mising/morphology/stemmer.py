"""
Stemming and lemmatization for Mising agglutinative morphology.

Mising morphology is predominantly agglutinative and suffixing. Nouns take
plural markers followed by case markers, while verbs take aspect, tense, mood,
and negative markers.

This module provides rule-based stemming with configurable aggressiveness levels.
"""

from enum import Enum
from typing import List, Optional
from mising.unicode_utils import normalize_mising_text


class StemmingMode(Enum):
    """
    Stemming aggressiveness levels.
    """
    LIGHT = "light"          # Strips only nominal case and plural suffixes
    MEDIUM = "medium"        # Strips case, plural, and verbal inflectional suffixes
    AGGRESSIVE = "aggressive"# Also strips derivational, negative, and nominalizer suffixes


# --- Suffix Lists ordered from longest to shortest for greedy match ---

# Case suffixes:
# Locative: -lo, -so, -do
# Ablative / Instrumental: -lokerang, -loke, -lok, -e
# Genitive: -ke, -k
# Accusative / Dative: -am, -m
# Allative / Purposive: -lodope, -pe
# Comitative: -kípe, -kipe, -bírpe, -kído, -rupe
CASE_SUFFIXES: List[str] = sorted([
    "-lokerang", "lokerang",
    "-lodope", "lodope",
    "-kípe", "kípe", "-kipe", "kipe",
    "-bírpe", "bírpe",
    "-kído", "kído",
    "-rupe", "rupe",
    "-loke", "loke",
    "-lok", "lok",
    "-lo", "lo",
    "-so", "so",
    "-do", "do",
    "-ke", "ke",
    "-pe", "pe",
    "-am", "am",
    "-m",
    "-e", "e",
], key=lambda x: len(x.lstrip("-")), reverse=True)

# Plural markers:
PLURAL_SUFFIXES: List[str] = sorted([
    "-kídíng", "kídíng", "-kíding", "kíding",
    "-kídí", "kídí", "-kidi", "kidi",
    "-bula", "bula",
    "-miíŋ", "miíŋ", "-miing", "miing",
], key=lambda x: len(x.lstrip("-")), reverse=True)

# Verbal inflectional suffixes (Tense, Aspect, Mood):
VERBAL_INFLECTION_SUFFIXES: List[str] = sorted([
    # Aspect / Tense
    "-duŋ-ma", "duŋ-ma", "-dung-ma", "dung-ma",
    "-duŋ", "duŋ", "-dung", "dung",  # Continuous / non-past
    "-tokai", "tokai",               # Remote past
    "-toka", "toka",                 # Present perfect
    "-to", "to",                     # Past simple
    "-kai", "kai",                   # Past / completive
    "-ka", "ka",                     # Perfect
    "-ye", "ye", "-yé", "yé",        # Future / Intentional
    # Mood / Imperatives
    "-tangka", "tangka",
    "-tola", "tola",
    "-lang", "lang",                 # Imperative
    "-yopé", "yopé", "-yope", "yope",# Prohibitive
    "-mopa", "mopa",
], key=lambda x: len(x.lstrip("-")), reverse=True)

# Verbal derivational / negation / participle suffixes:
VERBAL_DERIVATION_SUFFIXES: List[str] = sorted([
    "-mangkai", "mangkai",
    "-mange", "mange",
    "-mang", "mang",
    "-ma", "ma",                     # Negation
    "-nam", "nam",                   # Gerund / Nominalizer (e.g. men-nam -> speech)
    "-ne", "ne",                     # Agentive / Habitual (e.g. ger-ne -> singer)
    "-dola", "dola",
    "-sin", "sin",
    "-la", "la",                     # Converb
], key=lambda x: len(x.lstrip("-")), reverse=True)


class MisingStemmer:
    """
    Mising stemmer and lemmatizer.

    Args:
        mode: Stemming aggressiveness (LIGHT, MEDIUM, AGGRESSIVE). Default is MEDIUM.
        min_stem_length: Minimum character length to protect short root words
                         (like 'do' [eat], 'gi' [go], 'ti' [drink], 'in' [come]).
    """

    def __init__(self, mode: StemmingMode = StemmingMode.MEDIUM, min_stem_length: int = 2):
        self.mode = mode
        self.min_stem_length = min_stem_length

    def stem(self, word: str) -> str:
        """
        Extract the stem or root of a Mising word.

        Args:
            word: Input word token (e.g. 'ami-kídí-lo', 'gerduŋ', 'donam').

        Returns:
            The stemmed base form.

        Examples:
            >>> stemmer = MisingStemmer()
            >>> stemmer.stem("ami-kídí-lo")
            'ami'
            >>> stemmer.stem("gerduŋ")
            'ger'
            >>> stemmer.stem("okum-lo")
            'okum'
        """
        if not word:
            return ""

        original = normalize_mising_text(word.strip())
        lowered = original.lower()

        # Handle pronoun accusative forms
        PRONOUN_ACCUSATIVE = {
            "ngom": "ngo",
            "nom": "no",
            "bim": "bi",
            "bulum": "bulu",
            "ngolum": "ngolu",
            "nolum": "nolu",
        }
        if lowered in PRONOUN_ACCUSATIVE:
            return PRONOUN_ACCUSATIVE[lowered]

        # Handle hyphenated compound prefixes/clitics directly:
        # e.g. "ami-kídí" -> "ami", "ger-duŋ" -> "ger"
        if "-" in lowered:
            parts = lowered.split("-")
            # If the head root is the first element
            if len(parts[0]) >= self.min_stem_length:
                # Check if subsequent parts are known suffixes
                all_suffixes = (
                    CASE_SUFFIXES + PLURAL_SUFFIXES +
                    VERBAL_INFLECTION_SUFFIXES + VERBAL_DERIVATION_SUFFIXES
                )
                clean_suffs = {s.lstrip("-") for s in all_suffixes}
                if all(p in clean_suffs for p in parts[1:]):
                    return parts[0]

        current = lowered

        # In MEDIUM / AGGRESSIVE mode, if word ends with a finite verbal inflection,
        # prioritize verbal inflections (e.g. gerduŋ -> ger, gerto -> ger, gerye -> ger)
        if self.mode in (StemmingMode.MEDIUM, StemmingMode.AGGRESSIVE):
            if self.mode == StemmingMode.AGGRESSIVE:
                current = self._strip_suffix_group(
                    current,
                    ["-mangkai", "mangkai", "-mange", "mange", "-mang", "mang", "-ma", "ma"],
                )

            v_stripped = self._strip_suffix_group(current, VERBAL_INFLECTION_SUFFIXES)
            if v_stripped != current:
                current = v_stripped
                return current.rstrip("-")

        # Step 1: Strip case suffixes (avoiding false matches for 'am' inside 'nam', or 'e' inside 'ye'/'ne')
        current = self._strip_case_suffixes(current)

        # Step 2: Strip plural suffixes
        current = self._strip_suffix_group(current, PLURAL_SUFFIXES)

        # Step 3: Strip verbal inflections (if not already handled)
        if self.mode in (StemmingMode.MEDIUM, StemmingMode.AGGRESSIVE):
            current = self._strip_suffix_group(current, VERBAL_INFLECTION_SUFFIXES)

        # Step 4: Strip derivational and negation suffixes (if mode is AGGRESSIVE)
        if self.mode == StemmingMode.AGGRESSIVE:
            current = self._strip_suffix_group(current, VERBAL_DERIVATION_SUFFIXES)

        # Clean trailing hyphens or empty residue
        current = current.rstrip("-")

        if len(current) < self.min_stem_length:
            return lowered.rstrip("-")

        return current

    def _strip_case_suffixes(self, word: str) -> str:
        """Strip nominal case suffixes while guarding against clashing verbal/derivational substrings."""
        for suff in CASE_SUFFIXES:
            # If suffix entry requires a hyphen (e.g. "-m"), only match with hyphen
            if suff.startswith("-") and suff[1:] not in CASE_SUFFIXES:
                clean = suff[1:]
                if word.endswith("-" + clean):
                    remainder = word[:-(len(clean) + 1)]
                    if len(remainder) >= self.min_stem_length:
                        return remainder
                continue

            clean = suff.lstrip("-")
            # Protect -nam from -am or -m
            if clean in ("am", "m") and (word.endswith("nam") or word.endswith("-nam")):
                continue
            # Protect -ye, -yé, -ne from -e
            if clean == "e" and (word.endswith("ye") or word.endswith("yé") or word.endswith("ne")):
                continue

            # Check with hyphen
            if word.endswith("-" + clean):
                remainder = word[:-(len(clean) + 1)]
                if len(remainder) >= self.min_stem_length:
                    return remainder
            # Check without hyphen
            elif word.endswith(clean):
                remainder = word[:-len(clean)]
                if len(remainder) >= self.min_stem_length:
                    return remainder
        return word

    def _strip_suffix_group(self, word: str, suffixes: List[str]) -> str:
        """Helper to test and strip any matching suffix in a group while respecting min length."""
        for suff in suffixes:
            clean = suff.lstrip("-")
            # Check with hyphen
            if word.endswith("-" + clean):
                remainder = word[:-(len(clean) + 1)]
                if len(remainder) >= self.min_stem_length:
                    return remainder
            # Check without hyphen
            elif word.endswith(clean):
                remainder = word[:-len(clean)]
                if len(remainder) >= self.min_stem_length:
                    return remainder
        return word


def stem(word: str, mode: StemmingMode = StemmingMode.MEDIUM) -> str:
    """
    Convenience function to stem a single word.

    Args:
        word: Word token to stem.
        mode: StemmingMode (default MEDIUM).

    Returns:
        Stemmed word string.
    """
    return MisingStemmer(mode=mode).stem(word)
