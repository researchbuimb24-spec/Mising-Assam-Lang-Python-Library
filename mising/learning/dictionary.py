"""
Bilingual and trilingual dictionary for Mising (Mising - English - Assamese).
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Union
from mising.unicode_utils import normalize_mising_text


@dataclass
class DictionaryEntry:
    """Represents a structured dictionary entry for a Mising lemma."""
    mising: str
    pos: str
    english: str
    assamese: str
    ipa: str = ""
    examples: List[Dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Union[str, List[Dict[str, str]]]]:
        return {
            "mising": self.mising,
            "pos": self.pos,
            "english": self.english,
            "assamese": self.assamese,
            "ipa": self.ipa,
            "examples": self.examples,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "DictionaryEntry":
        return cls(
            mising=data["mising"],
            pos=data.get("pos", "NOUN"),
            english=data.get("english", ""),
            assamese=data.get("assamese", ""),
            ipa=data.get("ipa", ""),
            examples=data.get("examples", []),
        )


# Comprehensive foundational dictionary entries
DEFAULT_ENTRIES: List[DictionaryEntry] = [
    DictionaryEntry(
        mising="ami",
        pos="NOUN",
        english="person, human being, man",
        assamese="মানুহ, ব্যক্তি",
        ipa="ami",
        examples=[{"mising": "Ami kampo", "english": "Good person", "assamese": "ভাল মানুহ"}],
    ),
    DictionaryEntry(
        mising="agom",
        pos="NOUN",
        english="word, speech, language",
        assamese="ভাষা, কথা",
        ipa="aɡom",
        examples=[{"mising": "Mising agom", "english": "Mising language", "assamese": "মিচিং ভাষা"}],
    ),
    DictionaryEntry(
        mising="okum",
        pos="NOUN",
        english="house, home, dwelling",
        assamese="ঘৰ, গৃহ",
        ipa="okum",
        examples=[{"mising": "Ngo okumlo giduŋ", "english": "I am going home", "assamese": "মই ঘৰলৈ গৈছোঁ"}],
    ),
    DictionaryEntry(
        mising="asi",
        pos="NOUN",
        english="water, river, fluid",
        assamese="পানী, নদী",
        ipa="asi",
        examples=[{"mising": "Asi titoka", "english": "Drank water", "assamese": "পানী খালে"}],
    ),
    DictionaryEntry(
        mising="apong",
        pos="NOUN",
        english="traditional fermented rice beverage / brew",
        assamese="আপং, চাউলৰ মদ",
        ipa="apoŋ",
        examples=[{"mising": "Apong tila gernam gerto", "english": "Drank apong and sang songs", "assamese": "আপং খাই গান গালে"}],
    ),
    DictionaryEntry(
        mising="doolung",
        pos="NOUN",
        english="village, settlement",
        assamese="গাঁও, বসতি",
        ipa="doːluŋ",
        examples=[{"mising": "Doolunglo mosumduŋ", "english": "Working in the village", "assamese": "গাঁৱত কাম কৰিছে"}],
    ),
    DictionaryEntry(
        mising="do",
        pos="VERB",
        english="to eat, consume food",
        assamese="খোৱা",
        ipa="do",
        examples=[{"mising": "Apin doduŋ", "english": "Eating rice", "assamese": "ভাত খাই আছে"}],
    ),
    DictionaryEntry(
        mising="ti",
        pos="VERB",
        english="to drink",
        assamese="খোৱা / পান কৰা",
        ipa="ti",
        examples=[{"mising": "Asi tiduŋ", "english": "Drinking water", "assamese": "পানী খাই আছে"}],
    ),
    DictionaryEntry(
        mising="gi",
        pos="VERB",
        english="to go, walk, depart",
        assamese="যোৱা",
        ipa="ɡi",
        examples=[{"mising": "Kolo giduŋ?", "english": "Where are you going?", "assamese": "ক'লৈ গৈছা?"}],
    ),
    DictionaryEntry(
        mising="in",
        pos="VERB",
        english="to come, arrive",
        assamese="আহা",
        ipa="in",
        examples=[{"mising": "Inlang!", "english": "Come here!", "assamese": "আহা!"}],
    ),
    DictionaryEntry(
        mising="men",
        pos="VERB",
        english="to speak, talk, utter",
        assamese="কোৱা, কথা পতা",
        ipa="men",
        examples=[{"mising": "Agom menduŋ", "english": "Speaking words", "assamese": "কথা কৈ আছে"}],
    ),
    DictionaryEntry(
        mising="kampo",
        pos="ADJ",
        english="good, beautiful, fine, auspicious",
        assamese="ভাল, ধুনীয়া",
        ipa="kampo",
        examples=[{"mising": "Kampope kaduŋ", "english": "I am fine", "assamese": "ভালে আছোঁ"}],
    ),
    DictionaryEntry(
        mising="kénam",
        pos="ADJ",
        english="knowing, wise, knowledgeable",
        assamese="জ্ঞানী, জনা",
        ipa="kənam",
        examples=[{"mising": "Kénam ami", "english": "Wise person", "assamese": "জ্ঞানী মানুহ"}],
    ),
    DictionaryEntry(
        mising="ngo",
        pos="PRON",
        english="I, 1st person singular pronoun",
        assamese="মই",
        ipa="ŋo",
        examples=[{"mising": "Ngo giduŋ", "english": "I am going", "assamese": "মই গৈছোঁ"}],
    ),
    DictionaryEntry(
        mising="no",
        pos="PRON",
        english="you, 2nd person singular pronoun",
        assamese="তুমি / তই",
        ipa="no",
        examples=[{"mising": "No inlang", "english": "You come", "assamese": "তুমি আহা"}],
    ),
    DictionaryEntry(
        mising="bi",
        pos="PRON",
        english="he, she, 3rd person singular pronoun",
        assamese="সি / তাই / তেওঁ",
        ipa="bi",
        examples=[{"mising": "Bi doduŋ", "english": "He/she is eating", "assamese": "সি খাই আছে"}],
    ),
]


class MisingDictionary:
    """
    Searchable Mising dictionary supporting English and Assamese translations.
    """

    def __init__(self, entries: Optional[List[DictionaryEntry]] = None):
        self._entries_by_mising: Dict[str, DictionaryEntry] = {}
        self._all_entries: List[DictionaryEntry] = []

        initial_entries = entries or DEFAULT_ENTRIES
        for entry in initial_entries:
            self.add_entry(entry)

    def add_entry(self, entry: DictionaryEntry) -> None:
        key = normalize_mising_text(entry.mising).lower()
        self._entries_by_mising[key] = entry
        self._all_entries.append(entry)

    def __len__(self) -> int:
        return len(self._entries_by_mising)

    def lookup(self, word: str) -> Optional[DictionaryEntry]:
        """Exact lookup by Mising word (case-insensitive)."""
        key = normalize_mising_text(word).strip().lower()
        return self._entries_by_mising.get(key)

    def search_english(self, query: str) -> List[DictionaryEntry]:
        """Search definitions for an English keyword."""
        q = query.strip().lower()
        return [e for e in self._all_entries if q in e.english.lower()]

    def search_assamese(self, query: str) -> List[DictionaryEntry]:
        """Search definitions for an Assamese keyword."""
        q = query.strip()
        return [e for e in self._all_entries if q in e.assamese]

    def prefix_search(self, prefix: str) -> List[DictionaryEntry]:
        """Find all Mising words starting with the given prefix."""
        p = normalize_mising_text(prefix).lower()
        return [e for e in self._all_entries if e.mising.lower().startswith(p)]

    def export_json(self, filepath: Union[str, Path]) -> None:
        """Export dictionary entries to JSON."""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = [e.to_dict() for e in self._all_entries]
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, filepath: Union[str, Path]) -> "MisingDictionary":
        """Load dictionary entries from JSON."""
        path = Path(filepath)
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        entries = [DictionaryEntry.from_dict(d) for d in data]
        return cls(entries=entries)


def get_default_dictionary() -> MisingDictionary:
    """Return the pre-loaded standard Mising dictionary."""
    return MisingDictionary()
