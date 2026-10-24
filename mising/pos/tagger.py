"""
Part-of-Speech Tagger for the Mising language.

Implements a hybrid rule-based and morphological POS tagger conforming to the
Universal Dependencies (UD) tagset:
  - NOUN: Noun
  - VERB: Verb
  - ADJ: Adjective
  - ADV: Adverb
  - PRON: Pronoun
  - NUM: Numeral
  - DET: Determiner
  - ADP: Adposition / Postposition
  - CCONJ: Coordinating Conjunction
  - SCONJ: Subordinating Conjunction
  - PART: Particle
  - INTJ: Interjection
  - PUNCT: Punctuation
  - SYM: Symbol
  - X: Other / Unknown
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from mising.tokenization import word_tokenize
from mising.unicode_utils import normalize_mising_text


# --- Lexicon of Closed and High-Frequency Open Class Words in Mising ---

CORE_LEXICON: Dict[str, str] = {
    # Pronouns (PRON)
    "ngo": "PRON", "ngom": "PRON", "ngok": "PRON", "ngoke": "PRON",
    "ngolu": "PRON", "ngoluk": "PRON", "ngolum": "PRON",
    "no": "PRON", "nom": "PRON", "nok": "PRON", "noke": "PRON",
    "nolu": "PRON", "noluk": "PRON", "nolum": "PRON",
    "bi": "PRON", "bim": "PRON", "bik": "PRON", "bike": "PRON",
    "bulu": "PRON", "buluk": "PRON", "bulum": "PRON",
    # Demonstratives
    "si": "PRON", "de": "PRON", "éde": "PRON", "ede": "PRON",
    "so": "ADV", "do": "ADV",
    # Interrogatives
    "séko": "PRON", "seko": "PRON",
    "heko": "PRON", "héko": "PRON",
    "inno": "PRON",
    "kolo": "ADV", "hékpe": "ADV", "hekpe": "ADV", "kappé": "ADV",
    "tédílo": "ADV", "tedilo": "ADV",

    # Numerals (NUM)
    "ako": "NUM", "anyi": "NUM", "aum": "NUM", "api": "NUM", "ango": "NUM",
    "akké": "NUM", "akkey": "NUM", "kinid": "NUM", "pini": "NUM",
    "konang": "NUM", "iing": "NUM", "ying": "NUM", "eeng": "NUM",
    "lingko": "NUM", "linganyi": "NUM",

    # Common Nouns (NOUN)
    "ami": "NOUN", "mising": "NOUN", "agom": "NOUN", "okum": "NOUN",
    "asi": "NOUN", "apong": "NOUN", "ane": "NOUN", "abu": "NOUN",
    "ao": "NOUN", "omé": "NOUN", "ome": "NOUN", "yayo": "NOUN",
    "kaki": "NOUN", "doolung": "NOUN", "dolung": "NOUN", "ali": "NOUN",
    "aye": "NOUN", "lutad": "NOUN", "poro": "NOUN", "sine": "NOUN",
    "ékké": "NOUN", "ekke": "NOUN", "simyo": "NOUN", "amso": "NOUN",
    "kaban": "NOUN", "doying": "NOUN", "do:ying": "NOUN", "kébang": "NOUN",
    "kebang": "NOUN", "dírbí": "NOUN", "dirbi": "NOUN", "asom": "NOUN",

    # Common Verbs (Roots) (VERB)
    "do": "VERB", "ti": "VERB", "gi": "VERB", "in": "VERB",
    "men": "VERB", "mi": "VERB", "ka": "VERB", "ger": "VERB",
    "mosum": "VERB", "kur": "VERB", "yarto": "VERB", "tén": "VERB",
    "inlang": "VERB", "gelang": "VERB",

    # Adjectives (ADJ)
    "kampo": "ADJ", "kénam": "ADJ", "kenam": "ADJ", "yamyar": "ADJ",
    "pube": "ADJ", "yasang": "ADJ", "tabor": "ADJ", "botte": "ADJ",
    "kero": "ADJ", "kadeng": "ADJ", "kídag": "ADJ",

    # Adverbs (ADV)
    "ténto": "ADV", "teto": "ADV", "melo": "ADV", "yelo": "ADV",
    "aralo": "ADV", "angodo": "ADV", "dégro": "ADV", "degro": "ADV",

    # Adpositions / Case clitics (ADP)
    "lo": "ADP", "lok": "ADP", "loke": "ADP", "ke": "ADP",
    "pe": "ADP", "kípe": "ADP", "kipe": "ADP", "bírpe": "ADP",

    # Conjunctions (CCONJ, SCONJ)
    "gí": "CCONJ", "gi": "CCONJ", "delo": "CCONJ", "arumpalo": "CCONJ",
    "em": "SCONJ", "delomin": "SCONJ",

    # Particles (PART)
    "sin": "PART", "ye": "PART", "ai": "PART", "da": "PART", "na": "PART", "le": "PART",

    # Interjections (INTJ)
    "oi": "INTJ", "hai": "INTJ", "kuye": "INTJ", "yo": "INTJ", "ohe": "INTJ",
}

# Numeral Classifiers in Mising (often followed by numeral like 'gor-ako', 'abor-anyi')
CLASSIFIERS = {"gor", "abor", "bor", "bar", "kol", "pat", "pum", "míki"}

# Punctuation set
PUNCTUATION_CHARS = set(".,!?:;\"'()[]{}-—–/<>।॥@#$%^&*")


class MisingPOSTagger:
    """
    Part-of-Speech Tagger for Mising text.

    Supports rule-based tagging, custom training on tagged corpus data,
    and serialized models.
    """

    def __init__(self, custom_lexicon: Optional[Dict[str, str]] = None):
        self.lexicon = dict(CORE_LEXICON)
        if custom_lexicon:
            self.lexicon.update({k.lower(): v for k, v in custom_lexicon.items()})

        # Transition probabilities or statistical priors (optional for trained models)
        self.transition_counts: Dict[str, Dict[str, int]] = {}
        self.tag_counts: Dict[str, int] = {}

    def tag_token(self, token: str, prev_tag: Optional[str] = None) -> str:
        """
        Determine the POS tag for a single token given its local context.

        Args:
            token: The word or punctuation token.
            prev_tag: The tag of the immediately preceding token (optional context).

        Returns:
            A Universal POS tag string (e.g. 'NOUN', 'VERB', 'PRON').
        """
        if not token:
            return "X"

        # 1. Punctuation
        if all(c in PUNCTUATION_CHARS for c in token):
            return "PUNCT"

        # 2. Pure Numbers
        if token.replace(".", "").replace(",", "").isdigit():
            return "NUM"

        lowered = normalize_mising_text(token).lower()

        # 3. Direct Lexicon Match
        if lowered in self.lexicon:
            return self.lexicon[lowered]

        # 4. Numeral classifier compounds (e.g. gor-ako, abor-anyi, pat-aum)
        if "-" in lowered:
            parts = lowered.split("-")
            if parts[0] in CLASSIFIERS and parts[-1] in ("ako", "anyi", "aum", "api", "ango"):
                return "NUM"

        # 5. Morphological Suffix Rules for OOV (Out-of-Vocabulary) words
        # Verbal suffixes: -duŋ, -dung, -to, -ye, -yé, -lang, -ka, -toka, -tokai, -kai
        verb_suffixes = (
            "duŋ", "dung", "tokai", "toka", "to", "kai", "ka",
            "ye", "yé", "lang", "tangka", "yopé", "mopa"
        )
        for vs in verb_suffixes:
            if lowered.endswith("-" + vs) or (len(lowered) >= len(vs) + 2 and lowered.endswith(vs)):
                return "VERB"

        # Nominalizer: -nam (e.g. mennam [speech], donam [food], ginam [walk])
        if lowered.endswith("nam") or lowered.endswith("-nam"):
            return "NOUN"

        # Plural and Case suffixes: -kídí, -kídíng, -bula, -lo, -lok, -ke, -am
        nominal_suffixes = (
            "-kídí", "kídí", "-kidi", "kidi", "-kídíng", "kídíng", "-bula", "bula",
            "-lokerang", "lokerang", "-lodope", "lodope",
            "-lok", "-loke", "-lo", "-so", "-do", "-ke", "-am", "-pe"
        )
        for ns in nominal_suffixes:
            if lowered.endswith(ns):
                return "NOUN"

        # 6. Negative verbal forms (-mang, -ma, -mangkai)
        if lowered.endswith("mangkai") or lowered.endswith("mang") or lowered.endswith("-ma"):
            return "VERB"

        # 7. Context heuristics:
        # After a pronoun subject (e.g. "ngo", "no", "bi"), an unknown word is often a VERB or NOUN
        if prev_tag == "PRON":
            return "VERB"

        # Default fallback for open-class content words in Mising
        return "NOUN"

    def tag(self, tokens: List[str]) -> List[Tuple[str, str]]:
        """
        Tag a sequence of tokens.

        Args:
            tokens: List of string tokens.

        Returns:
            List of (token, pos_tag) pairs.

        Examples:
            >>> tagger = MisingPOSTagger()
            >>> tagger.tag(['Ngo', 'okum-lo', 'giduŋ', '.'])
            [('Ngo', 'PRON'), ('okum-lo', 'NOUN'), ('giduŋ', 'VERB'), ('.', 'PUNCT')]
        """
        tagged: List[Tuple[str, str]] = []
        prev_tag: Optional[str] = None

        for tok in tokens:
            t = self.tag_token(tok, prev_tag)
            tagged.append((tok, t))
            prev_tag = t

        return tagged

    def tag_text(self, text: str) -> List[Tuple[str, str]]:
        """
        Tokenize and tag raw Mising text.

        Args:
            text: Input string.

        Returns:
            List of (token, tag) pairs.
        """
        tokens = word_tokenize(text)
        return self.tag(tokens)

    def train(self, tagged_sentences: List[List[Tuple[str, str]]]) -> None:
        """
        Learn word frequencies and transitions from a tagged corpus.

        Args:
            tagged_sentences: List of sentences, where each sentence is a list
                              of (word, tag) tuples.
        """
        word_tag_counts: Dict[str, Dict[str, int]] = {}

        for sent in tagged_sentences:
            prev_tag = "<START>"
            for word, tag in sent:
                norm_word = normalize_mising_text(word).lower()
                word_tag_counts.setdefault(norm_word, {})
                word_tag_counts[norm_word][tag] = word_tag_counts[norm_word].get(tag, 0) + 1

                self.transition_counts.setdefault(prev_tag, {})
                self.transition_counts[prev_tag][tag] = (
                    self.transition_counts[prev_tag].get(tag, 0) + 1
                )
                self.tag_counts[tag] = self.tag_counts.get(tag, 0) + 1
                prev_tag = tag

        # Update lexicon with most frequent tag per word
        for word, tcounts in word_tag_counts.items():
            best_tag = max(tcounts.items(), key=lambda kv: kv[1])[0]
            self.lexicon[word] = best_tag

    def save_model(self, filepath: Union[str, Path]) -> None:
        """Save learned lexicon and transition counts to JSON."""
        data = {
            "lexicon": self.lexicon,
            "transition_counts": self.transition_counts,
            "tag_counts": self.tag_counts,
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_model(self, filepath: Union[str, Path]) -> None:
        """Load lexicon and counts from JSON file."""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.lexicon = data.get("lexicon", {})
        self.transition_counts = data.get("transition_counts", {})
        self.tag_counts = data.get("tag_counts", {})


def pos_tag(text_or_tokens: Union[str, List[str]]) -> List[Tuple[str, str]]:
    """
    Convenience function to POS tag Mising text or pre-tokenized words.

    Args:
        text_or_tokens: Either a raw string or a list of token strings.

    Returns:
        List of (token, tag) tuples.
    """
    tagger = MisingPOSTagger()
    if isinstance(text_or_tokens, str):
        return tagger.tag_text(text_or_tokens)
    return tagger.tag(text_or_tokens)
