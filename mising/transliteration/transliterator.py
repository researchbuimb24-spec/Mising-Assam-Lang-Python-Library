"""
Bidirectional transliteration engine for Mising.

Supports conversions between:
1. 'mising_latin' (MAK Roman standard with 'é', 'í', 'ng', 'ny')
2. 'assamese' (Assamese script / অসমীয়া লিপি)
3. 'ascii' (Simplified ASCII Latin with apostrophes: 'e'', 'i'')
4. 'ipa' (International Phonetic Alphabet)
"""

import re
from typing import Dict, List, Tuple
from mising.unicode_utils import normalize_mising_text


# --- Mising Roman <-> Assamese Script Mapping Tables ---

# Consonants (Digraphs first for greedy matching)
MISING_CONSONANTS_TO_AS: List[Tuple[str, str]] = [
    ("kh", "খ"),
    ("th", "থ"),
    ("ph", "ফ"),
    ("ng", "ঙ"),
    ("ny", "ঞ"),
    ("ch", "ছ"),
    ("k", "ক"),
    ("g", "গ"),
    ("c", "চ"),
    ("j", "জ"),
    ("t", "ত"),
    ("d", "দ"),
    ("n", "ন"),
    ("p", "প"),
    ("b", "ব"),
    ("m", "ম"),
    ("y", "য"),
    ("r", "ৰ"),
    ("l", "ল"),
    ("s", "স"),
    ("h", "হ"),
    ("w", "ৱ"),
]

# Independent Vowels (word-initial or following a vowel)
MISING_VOWELS_INDEP_TO_AS: List[Tuple[str, str]] = [
    ("aa", "আ"),
    ("éé", "এ'"),
    ("íí", "ই'"),
    ("ii", "ঈ"),
    ("uu", "ঊ"),
    ("ee", "এ"),
    ("oo", "ও"),
    ("é", "এ'"),   # Central vowel /ə/
    ("í", "ই'"),   # Central vowel /ɨ/
    ("a", "আ"),
    ("i", "ই"),
    ("u", "উ"),
    ("e", "এ"),
    ("o", "অ"),
]

# Dependent Vowel Signs (Matras) following a consonant
MISING_VOWELS_MATRA_TO_AS: List[Tuple[str, str]] = [
    ("aa", "া"),
    ("éé", "ে'"),
    ("íí", "ি'"),
    ("ii", "ী"),
    ("uu", "ূ"),
    ("ee", "ে"),
    ("oo", "ো"),
    ("é", "ে'"),
    ("í", "ি'"),
    ("a", "া"),
    ("i", "ি"),
    ("u", "ু"),
    ("e", "ে"),
    ("o", "ো"),
]

# Assamese Script to Mising Latin mapping
AS_TO_MISING_VOWEL_INDEP: Dict[str, str] = {
    "অ": "o",
    "আ": "a",
    "ই": "i",
    "ঈ": "ii",
    "উ": "u",
    "ঊ": "uu",
    "এ": "e",
    "ঐ": "oi",
    "ও": "oo",
    "ঔ": "ou",
}

AS_TO_MISING_MATRA: Dict[str, str] = {
    "া": "a",
    "ি": "i",
    "ী": "ii",
    "ু": "u",
    "ূ": "uu",
    "ে": "e",
    "ৈ": "oi",
    "ো": "oo",
    "ৌ": "ou",
    "্": "",   # Virama / hasanta
}

AS_TO_MISING_CONSONANTS: Dict[str, str] = {
    "ক": "k", "খ": "kh", "গ": "g", "ঘ": "gh", "ঙ": "ng", "ং": "ng",
    "চ": "c", "ছ": "ch", "জ": "j", "ঝ": "jh", "ঞ": "ny",
    "ট": "t", "ঠ": "th", "ড": "d", "ঢ": "dh", "ণ": "n",
    "ত": "t", "থ": "th", "দ": "d", "ধ": "dh", "ন": "n",
    "প": "p", "ফ": "ph", "ব": "b", "ভ": "bh", "ম": "m",
    "য": "y", "য়": "y", "ৰ": "r", "ল": "l", "ৱ": "w",
    "শ": "s", "ষ": "s", "স": "s", "হ": "h", "ক্ষ": "khy",
}

# IPA mappings for Mising
IPA_MAPPING: List[Tuple[str, str]] = [
    ("aa", "aː"),
    ("éé", "əː"),
    ("íí", "ɨː"),
    ("ii", "iː"),
    ("uu", "uː"),
    ("ee", "eː"),
    ("oo", "oː"),
    ("é", "ə"),
    ("í", "ɨ"),
    ("ng", "ŋ"),
    ("ny", "ɲ"),
    ("kh", "kʰ"),
    ("th", "tʰ"),
    ("ph", "pʰ"),
    ("c", "tʃ"),
    ("j", "dʒ"),
    ("y", "j"),
    ("r", "ɾ"),
]


class MisingTransliterator:
    """
    Transliterator supporting Mising Roman, Assamese, ASCII, and IPA scripts.
    """

    @classmethod
    def mising_to_assamese(cls, text: str) -> str:
        """
        Transliterate Mising Roman text (MAK standard) to Assamese script.

        Args:
            text: Input string in Mising Roman script.

        Returns:
            String rendered in Assamese script.

        Examples:
            >>> MisingTransliterator.mising_to_assamese("Mising")
            'মিচিং'
            >>> MisingTransliterator.mising_to_assamese("okum-lo")
            'ওকুম্-লো'
        """
        if not text:
            return ""

        text = normalize_mising_text(text)
        result: List[str] = []
        i = 0
        n = len(text)

        consonant_dict = dict(MISING_CONSONANTS_TO_AS)
        consonant_keys = sorted(consonant_dict.keys(), key=len, reverse=True)
        vowel_indep_keys = sorted([k for k, _ in MISING_VOWELS_INDEP_TO_AS], key=len, reverse=True)
        vowel_matra_dict = dict(MISING_VOWELS_MATRA_TO_AS)
        vowel_matra_keys = sorted(vowel_matra_dict.keys(), key=len, reverse=True)

        while i < n:
            ch = text[i]

            # Pass through whitespace, hyphens, and non-alphabetic chars
            if not ch.isalpha():
                if ch == ".":
                    result.append("।")
                else:
                    result.append(ch)
                i += 1
                continue

            low_rem = text[i:].lower()

            # Check for consonant at current position
            matched_c = None
            for c_cand in consonant_keys:
                if low_rem.startswith(c_cand):
                    matched_c = c_cand
                    break

            if matched_c:
                c_as = consonant_dict[matched_c]
                i += len(matched_c)
                low_rem = text[i:].lower()

                # Check if a vowel immediately follows this consonant
                matched_v = None
                for v_cand in vowel_matra_keys:
                    if low_rem.startswith(v_cand):
                        matched_v = v_cand
                        break

                if matched_v:
                    # Append consonant + dependent vowel matra
                    matra = vowel_matra_dict[matched_v]
                    result.append(c_as + matra)
                    i += len(matched_v)
                else:
                    # Consonant coda or preconsonantal: add virama (্) if at end of word or before another consonant
                    # Exception: if next is hyphen or end of word, add virama
                    if (
                        i == n
                        or text[i] in " -_.,!?:;\"'()[]"
                        or any(low_rem.startswith(cc) for cc in consonant_keys)
                    ):
                        result.append(c_as + "্")
                    else:
                        result.append(c_as)
            else:
                # Vowel at onset / initial / independent
                matched_v = None
                for v_cand in vowel_indep_keys:
                    if low_rem.startswith(v_cand):
                        matched_v = v_cand
                        break

                if matched_v:
                    indep_as = dict(MISING_VOWELS_INDEP_TO_AS)[matched_v]
                    result.append(indep_as)
                    i += len(matched_v)
                else:
                    # Other Latin character fallback
                    result.append(ch)
                    i += 1

        return "".join(result)

    @classmethod
    def assamese_to_mising(cls, text: str) -> str:
        """
        Transliterate Assamese script Mising text back to standard Roman orthography.

        Args:
            text: Input string in Assamese script.

        Returns:
            String rendered in Mising standard Roman orthography.

        Examples:
            >>> MisingTransliterator.assamese_to_mising("মিচিং")
            'micing'
        """
        if not text:
            return ""

        result: List[str] = []
        i = 0
        n = len(text)

        while i < n:
            ch = text[i]

            # Check for punctuation (e.g. danda)
            if ch == "।":
                result.append(".")
                i += 1
                continue
            if ch == "॥":
                result.append(".")
                i += 1
                continue

            # Check special combination: এ' / ই' / ে' / ি' (Mising central vowels)
            if i + 1 < n and text[i + 1] == "'":
                if ch == "এ":
                    result.append("é")
                    i += 2
                    continue
                elif ch == "ই":
                    result.append("í")
                    i += 2
                    continue
                elif ch == "ে":
                    result.append("é")
                    i += 2
                    continue
                elif ch == "ি":
                    result.append("í")
                    i += 2
                    continue

            # Independent vowels
            if ch in AS_TO_MISING_VOWEL_INDEP:
                result.append(AS_TO_MISING_VOWEL_INDEP[ch])
                i += 1
                continue

            # Consonants
            if ch in AS_TO_MISING_CONSONANTS:
                c_rom = AS_TO_MISING_CONSONANTS[ch]
                i += 1
                # Look ahead for matra or halant
                if i < n:
                    next_ch = text[i]
                    if i + 1 < n and text[i + 1] == "'":
                        if next_ch == "ে":
                            result.append(c_rom + "é")
                            i += 2
                            continue
                        elif next_ch == "ি":
                            result.append(c_rom + "í")
                            i += 2
                            continue

                    if next_ch in AS_TO_MISING_MATRA:
                        matra_rom = AS_TO_MISING_MATRA[next_ch]
                        result.append(c_rom + matra_rom)
                        i += 1
                    else:
                        result.append(c_rom)
                else:
                    result.append(c_rom)
                continue

            # Other characters (whitespace, numbers, etc.)
            result.append(ch)
            i += 1

        return "".join(result)

    @classmethod
    def mising_to_ipa(cls, text: str) -> str:
        """
        Convert Mising text to International Phonetic Alphabet (IPA).

        Examples:
            >>> MisingTransliterator.mising_to_ipa("ami-kídí")
            'ami-kɨdi'
            >>> MisingTransliterator.mising_to_ipa("apong")
            'apoŋ'
        """
        if not text:
            return ""

        text = normalize_mising_text(text).lower()
        res = text
        for src, ipa in IPA_MAPPING:
            res = res.replace(src, ipa)
        return res

    @classmethod
    def mising_to_ascii(cls, text: str) -> str:
        """
        Convert canonical Mising diacritic characters ('é', 'í') to ASCII friendly ('e'', 'i'').

        Examples:
            >>> MisingTransliterator.mising_to_ascii("ami-kídí")
            "ami-ki'di'"
        """
        if not text:
            return ""
        text = normalize_mising_text(text)
        return text.replace("é", "e'").replace("É", "E'").replace("í", "i'").replace("Í", "I'")

    @classmethod
    def ascii_to_mising(cls, text: str) -> str:
        """
        Convert ASCII representation with apostrophes ('e'', 'i'') to standard MAK diacritics.

        Examples:
            >>> MisingTransliterator.ascii_to_mising("ami-ki'di'")
            'ami-kídí'
        """
        if not text:
            return ""
        text = text.replace("e'", "é").replace("E'", "É").replace("i'", "í").replace("I'", "Í")
        return normalize_mising_text(text)


def transliterate(text: str, source: str = "mising", target: str = "assamese") -> str:
    """
    High-level transliteration dispatcher.

    Args:
        text: Input string.
        source: 'mising' (or 'latin'), 'assamese', 'ascii'.
        target: 'assamese', 'mising', 'ipa', 'ascii'.

    Returns:
        Transliterated string.
    """
    src = source.lower()
    tgt = target.lower()

    if src in ("mising", "latin", "roman"):
        if tgt in ("assamese", "as"):
            return MisingTransliterator.mising_to_assamese(text)
        elif tgt in ("ipa", "phonetic"):
            return MisingTransliterator.mising_to_ipa(text)
        elif tgt in ("ascii", "plain"):
            return MisingTransliterator.mising_to_ascii(text)
        return text

    elif src in ("assamese", "as"):
        mising_rom = MisingTransliterator.assamese_to_mising(text)
        if tgt in ("mising", "latin", "roman"):
            return mising_rom
        elif tgt == "ipa":
            return MisingTransliterator.mising_to_ipa(mising_rom)
        elif tgt == "ascii":
            return MisingTransliterator.mising_to_ascii(mising_rom)
        return text

    elif src in ("ascii", "plain"):
        mising_rom = MisingTransliterator.ascii_to_mising(text)
        if tgt in ("mising", "latin", "roman"):
            return mising_rom
        elif tgt in ("assamese", "as"):
            return MisingTransliterator.mising_to_assamese(mising_rom)
        elif tgt == "ipa":
            return MisingTransliterator.mising_to_ipa(mising_rom)
        return text

    return text


def mising_to_assamese(text: str) -> str:
    return MisingTransliterator.mising_to_assamese(text)


def assamese_to_mising(text: str) -> str:
    return MisingTransliterator.assamese_to_mising(text)


def mising_to_ipa(text: str) -> str:
    return MisingTransliterator.mising_to_ipa(text)


def mising_to_ascii(text: str) -> str:
    return MisingTransliterator.mising_to_ascii(text)


def ascii_to_mising(text: str) -> str:
    return MisingTransliterator.ascii_to_mising(text)
