"""
Morphological Analyzer for the Mising language.

Provides detailed segmentation, morpheme glossing (interlinear morpheme glosses
conforming to Leipzig Glossing Rules), and grammatical feature extraction.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from mising.unicode_utils import normalize_mising_text


@dataclass
class Morpheme:
    """Represents a single segmented morpheme."""
    surface: str       # Surface form (e.g. "-kídí")
    gloss: str         # Grammatical gloss (e.g. "PL")
    category: str      # Category: ROOT, CASE, PLURAL, TENSE, ASPECT, MOOD, NEG, NMLZ

    def __str__(self) -> str:
        return f"{self.surface}[{self.gloss}]"


@dataclass
class MorphAnalysis:
    """Represents the complete morphological analysis of a word."""
    word: str
    root: str
    morphemes: List[Morpheme] = field(default_factory=list)
    pos_hint: str = "NOUN"
    is_compound: bool = False
    features: Dict[str, str] = field(default_factory=dict)

    @property
    def gloss(self) -> str:
        """Return interlinear gloss string, e.g. ami-PL-LOC"""
        if not self.morphemes:
            return self.root
        parts = [self.root]
        for m in self.morphemes:
            parts.append(m.gloss)
        return "-".join(parts)

    def summary(self) -> str:
        """Human-readable explanation of morpheme components."""
        lines = [f"Word: {self.word}", f"Root: {self.root} ({self.pos_hint})"]
        if self.morphemes:
            lines.append("Morphemes:")
            for m in self.morphemes:
                lines.append(f"  • {m.surface} -> {m.gloss} ({m.category})")
        if self.features:
            feat_strs = [f"{k}={v}" for k, v in self.features.items()]
            lines.append("Features: " + ", ".join(feat_strs))
        return "\n".join(lines)


# Canonical gloss dictionary
GLOSS_DEFINITIONS: Dict[str, Tuple[str, str, Dict[str, str]]] = {
    # Nominal Case
    "lokerang": ("ABL", "CASE", {"case": "ablative"}),
    "lodope": ("ALL", "CASE", {"case": "allative"}),
    "kípe": ("COM", "CASE", {"case": "comitative"}),
    "kipe": ("COM", "CASE", {"case": "comitative"}),
    "bírpe": ("COM", "CASE", {"case": "comitative"}),
    "kído": ("COM", "CASE", {"case": "comitative"}),
    "rupe": ("COM", "CASE", {"case": "comitative"}),
    "loke": ("ABL/INST", "CASE", {"case": "ablative_instrumental"}),
    "lok": ("ABL/INST", "CASE", {"case": "ablative_instrumental"}),
    "lo": ("LOC", "CASE", {"case": "locative"}),
    "so": ("LOC", "CASE", {"case": "locative"}),
    "do": ("LOC", "CASE", {"case": "locative"}),
    "ke": ("GEN", "CASE", {"case": "genitive"}),
    "pe": ("ALL", "CASE", {"case": "allative"}),
    "am": ("ACC", "CASE", {"case": "accusative"}),
    "m": ("ACC", "CASE", {"case": "accusative"}),
    "ne": ("ERG", "CASE", {"case": "ergative"}),
    "e": ("ERG", "CASE", {"case": "ergative"}),

    # Plural
    "kídíng": ("PL", "PLURAL", {"number": "plural"}),
    "kíding": ("PL", "PLURAL", {"number": "plural"}),
    "kídí": ("PL", "PLURAL", {"number": "plural"}),
    "kidi": ("PL", "PLURAL", {"number": "plural"}),
    "bula": ("PL", "PLURAL", {"number": "plural"}),
    "miíŋ": ("PL", "PLURAL", {"number": "plural"}),
    "miing": ("PL", "PLURAL", {"number": "plural"}),

    # Verbal Tense/Aspect
    "duŋ": ("CONT", "ASPECT", {"aspect": "continuous", "tense": "present"}),
    "dung": ("CONT", "ASPECT", {"aspect": "continuous", "tense": "present"}),
    "tokai": ("PST.REM", "TENSE", {"tense": "past", "remoteness": "remote"}),
    "toka": ("PRF", "ASPECT", {"aspect": "perfect"}),
    "to": ("PST", "TENSE", {"tense": "past"}),
    "kai": ("PST", "TENSE", {"tense": "past"}),
    "ka": ("PRF", "ASPECT", {"aspect": "perfect"}),
    "ye": ("FUT", "TENSE", {"tense": "future"}),
    "yé": ("FUT", "TENSE", {"tense": "future"}),

    # Verbal Mood / Negation / Derivation
    "lang": ("IMP", "MOOD", {"mood": "imperative"}),
    "tangka": ("IMP", "MOOD", {"mood": "imperative"}),
    "tola": ("IMP", "MOOD", {"mood": "imperative"}),
    "yopé": ("PROH", "MOOD", {"mood": "prohibitive"}),
    "yope": ("PROH", "MOOD", {"mood": "prohibitive"}),
    "mopa": ("PROH", "MOOD", {"mood": "prohibitive"}),
    "mangkai": ("NEG.PST", "NEG", {"polarity": "negative", "tense": "past"}),
    "mange": ("NEG", "NEG", {"polarity": "negative"}),
    "mang": ("NEG", "NEG", {"polarity": "negative"}),
    "ma": ("NEG", "NEG", {"polarity": "negative"}),
    "nam": ("NMLZ", "DERIV", {"nominalizer": "gerund"}),
    "dola": ("CVB", "CONVERB", {"converb": "temporal"}),
    "sin": ("CVB", "CONVERB", {"converb": "concessive"}),
    "la": ("CVB", "CONVERB", {"converb": "sequential"}),
}


class MisingMorphAnalyzer:
    """
    Morphological parser for decomposing complex Mising word forms into
    root and grammatical morphemes.
    """

    def __init__(self, min_root_length: int = 2):
        self.min_root_length = min_root_length

    def analyze(self, word: str) -> MorphAnalysis:
        """
        Analyze a single word token.

        Args:
            word: Input word string (e.g. 'ami-kídí-lo', 'gerduŋ', 'donam-ke').

        Returns:
            MorphAnalysis containing roots, segmented morphemes, POS hint, and features.
        """
        if not word:
            return MorphAnalysis(word="", root="", pos_hint="X")

        norm_word = normalize_mising_text(word.strip())
        lowered = norm_word.lower()

        # Handle explicit hyphenation (e.g. ami-kídí-lo or do-nam)
        if "-" in lowered:
            return self._analyze_hyphenated(norm_word, lowered)

        return self._analyze_concatenated(norm_word, lowered)

    def _analyze_hyphenated(self, original: str, lowered: str) -> MorphAnalysis:
        parts = lowered.split("-")
        root = parts[0]
        morphemes: List[Morpheme] = []
        features: Dict[str, str] = {}
        pos_hint = "NOUN"

        is_compound = False
        # If second part is not in gloss definitions and looks like another noun/verb,
        # it's a compound word (e.g. ali-aye [seed-fruit])
        if len(parts) > 1 and parts[1] not in GLOSS_DEFINITIONS:
            is_compound = True

        for part in parts[1:]:
            if part in GLOSS_DEFINITIONS:
                gloss, cat, feats = GLOSS_DEFINITIONS[part]
                morphemes.append(Morpheme(surface="-" + part, gloss=gloss, category=cat))
                features.update(feats)
                if cat in ("TENSE", "ASPECT", "MOOD"):
                    pos_hint = "VERB"
            else:
                morphemes.append(Morpheme(surface="-" + part, gloss="STEM2", category="COMPOUND"))

        return MorphAnalysis(
            word=original,
            root=root,
            morphemes=morphemes,
            pos_hint=pos_hint,
            is_compound=is_compound,
            features=features,
        )

    def _analyze_concatenated(self, original: str, lowered: str) -> MorphAnalysis:
        # Check against sorted suffix candidates
        sorted_keys = sorted(GLOSS_DEFINITIONS.keys(), key=len, reverse=True)
        rem = lowered
        found_morphemes: List[Morpheme] = []
        features: Dict[str, str] = {}
        pos_hint = "NOUN"

        # Repeatedly peel suffixes from right to left
        progress = True
        while progress and len(rem) > self.min_root_length:
            progress = False
            for suff in sorted_keys:
                if rem.endswith(suff) and (len(rem) - len(suff)) >= self.min_root_length:
                    gloss, cat, feats = GLOSS_DEFINITIONS[suff]
                    found_morphemes.insert(
                        0, Morpheme(surface="-" + suff, gloss=gloss, category=cat)
                    )
                    features.update(feats)
                    if cat in ("TENSE", "ASPECT", "MOOD"):
                        pos_hint = "VERB"
                    rem = rem[:-len(suff)]
                    progress = True
                    break

        root = rem
        return MorphAnalysis(
            word=original,
            root=root,
            morphemes=found_morphemes,
            pos_hint=pos_hint,
            is_compound=False,
            features=features,
        )


def analyze(word: str) -> MorphAnalysis:
    """Convenience function for morphological analysis of a word."""
    return MisingMorphAnalyzer().analyze(word)
