"""
Thematic vocabulary lists for learning the Mising language.
"""

from typing import Dict, List, Optional


THEMATIC_VOCABULARY: Dict[str, List[Dict[str, str]]] = {
    "greetings": [
        {"mising": "Kuye", "english": "Hello / Greetings", "assamese": "নমস্কাৰ", "ipa": "kuje"},
        {"mising": "Oy", "english": "Yes", "assamese": "হয়", "ipa": "oj"},
        {"mising": "Mange", "english": "No / Not", "assamese": "নহয়", "ipa": "maŋe"},
        {"mising": "Kampope kídag gí?", "english": "How are you?", "assamese": "ভালে আছানে?", "ipa": "kampope kɨdaɡ ɡi"},
        {"mising": "Kampope kaduŋ", "english": "I am fine / Doing well", "assamese": "ভালে আছোঁ", "ipa": "kampope kaduŋ"},
        {"mising": "Yartola!", "english": "Goodbye! (Go well)", "assamese": "যাওঁদিয়া / বিদায়", "ipa": "jaɾtola"},
        {"mising": "Ami kampo", "english": "Good person", "assamese": "ভাল মানুহ", "ipa": "ami kampo"},
    ],
    "family": [
        {"mising": "Abu", "english": "Father", "assamese": "পিতা / দেউতা", "ipa": "abu"},
        {"mising": "Ane", "english": "Mother", "assamese": "আই / মা", "ipa": "ane"},
        {"mising": "Ao", "english": "Son / Child", "assamese": "ল'ৰা / সন্তান", "ipa": "ao"},
        {"mising": "Omé", "english": "Daughter / Girl", "assamese": "ছোৱালী", "ipa": "omə"},
        {"mising": "Babu", "english": "Elder brother", "assamese": "ককাইদেউ", "ipa": "babu"},
        {"mising": "Biro", "english": "Younger brother", "assamese": "ভাই", "ipa": "biɾo"},
        {"mising": "Bamo", "english": "Elder sister", "assamese": "বাইদেউ", "ipa": "bamo"},
        {"mising": "Birné", "english": "Younger sister", "assamese": "ভনী", "ipa": "biɾnə"},
        {"mising": "Yayo", "english": "Grandmother", "assamese": "আইতা", "ipa": "jajo"},
        {"mising": "Ata", "english": "Grandfather", "assamese": "ককা", "ipa": "ata"},
        {"mising": "Kaki", "english": "Maternal uncle", "assamese": "মোমাই", "ipa": "kaki"},
    ],
    "body_parts": [
        {"mising": "Dumbor", "english": "Head", "assamese": "মূৰ", "ipa": "dumboɾ"},
        {"mising": "Amik", "english": "Eye", "assamese": "চকু", "ipa": "amik"},
        {"mising": "Noroo", "english": "Ear", "assamese": "কাণ", "ipa": "noɾoː"},
        {"mising": "Nyobo", "english": "Nose", "assamese": "নাক", "ipa": "ɲobo"},
        {"mising": "Nappang", "english": "Mouth", "assamese": "মুখ", "ipa": "nappaŋ"},
        {"mising": "Ala", "english": "Hand / Arm", "assamese": "হাত", "ipa": "ala"},
        {"mising": "Léé", "english": "Leg / Foot", "assamese": "ভৰি", "ipa": "ləː"},
        {"mising": "Kí", "english": "Belly / Stomach", "assamese": "পেট", "ipa": "kɨ"},
        {"mising": "Apuk", "english": "Heart", "assamese": "হৃদয় / বুকু", "ipa": "apuk"},
    ],
    "nature": [
        {"mising": "Donyi", "english": "Sun", "assamese": "বেলি / সূৰ্য", "ipa": "doɲi"},
        {"mising": "Polo", "english": "Moon / Month", "assamese": "জোন / চন্দ্ৰ", "ipa": "polo"},
        {"mising": "Takir", "english": "Star", "assamese": "তৰা", "ipa": "takiɾ"},
        {"mising": "Taleng", "english": "Sky", "assamese": "আকাশ", "ipa": "taleŋ"},
        {"mising": "Asi", "english": "Water / River", "assamese": "পানী / নদী", "ipa": "asi"},
        {"mising": "Pídoo", "english": "Rain", "assamese": "বৰষুণ", "ipa": "pɨdoː"},
        {"mising": "Essar", "english": "Wind", "assamese": "বতাহ", "ipa": "essaɾ"},
        {"mising": "Émé", "english": "Fire", "assamese": "জুই", "ipa": "əmə"},
        {"mising": "Mído", "english": "Earth / Land", "assamese": "মাটি / পৃথিৱী", "ipa": "mɨdo"},
    ],
    "animals": [
        {"mising": "Sine", "english": "Elephant", "assamese": "হাতী", "ipa": "sine"},
        {"mising": "Simyo", "english": "Tiger", "assamese": "বাঘ", "ipa": "simjo"},
        {"mising": "Ékké", "english": "Dog", "assamese": "কুকুৰ", "ipa": "əkkə"},
        {"mising": "Ményo", "english": "Cat", "assamese": "মেকুৰী", "ipa": "mənjo"},
        {"mising": "Sho", "english": "Cow / Cattle", "assamese": "গৰু", "ipa": "ʃo"},
        {"mising": "Ég", "english": "Pig", "assamese": "গাহৰি", "ipa": "əɡ"},
        {"mising": "Poro", "english": "Hen / Chicken", "assamese": "কুকুৰা", "ipa": "poɾo"},
        {"mising": "Péttang", "english": "Bird", "assamese": "চৰাই", "ipa": "pəttaŋ"},
        {"mising": "Éngo", "english": "Fish", "assamese": "মাছ", "ipa": "əŋo"},
    ],
    "food_agriculture": [
        {"mising": "Apin", "english": "Cooked rice", "assamese": "ভাত", "ipa": "apin"},
        {"mising": "Apong", "english": "Traditional rice beverage", "assamese": "আপং / মদ", "ipa": "apoŋ"},
        {"mising": "Ali", "english": "Seed / Root", "assamese": "গুটি", "ipa": "ali"},
        {"mising": "Aye", "english": "Fruit", "assamese": "ফল", "ipa": "aje"},
        {"mising": "Oyíng", "english": "Vegetable / Curry", "assamese": "আঞ্জা / শাক-পাচলি", "ipa": "ojɨŋ"},
        {"mising": "Aluk", "english": "Salt", "assamese": "নিমখ", "ipa": "aluk"},
        {"mising": "Dírbí", "english": "Paddy field", "assamese": "পথাৰ", "ipa": "dɨɾbɨ"},
        {"mising": "Amso", "english": "Paddy grain", "assamese": "ধান", "ipa": "amso"},
    ],
    "time_calendar": [
        {"mising": "Silo", "english": "Today", "assamese": "আজি", "ipa": "silo"},
        {"mising": "Melo", "english": "Yesterday", "assamese": "কালি", "ipa": "melo"},
        {"mising": "Yelo", "english": "Tomorrow", "assamese": "কাইলৈ", "ipa": "jelo"},
        {"mising": "Arong", "english": "Morning", "assamese": "ৰাতিপুৱা", "ipa": "aɾoŋ"},
        {"mising": "Yombí", "english": "Evening", "assamese": "গধূলি", "ipa": "jombɨ"},
        {"mising": "Kammí", "english": "Night", "assamese": "ৰাতি", "ipa": "kammɨ"},
        {"mising": "Dísang", "english": "Year", "assamese": "বছৰ", "ipa": "dɨsaŋ"},
    ],
}


def list_themes() -> List[str]:
    """Return the list of available vocabulary themes."""
    return list(THEMATIC_VOCABULARY.keys())


def get_theme_vocabulary(theme: str) -> List[Dict[str, str]]:
    """
    Retrieve vocabulary words for a given theme.

    Args:
        theme: Theme name (e.g. 'greetings', 'family', 'animals').

    Returns:
        List of word dictionaries with keys 'mising', 'english', 'assamese', 'ipa'.
    """
    return THEMATIC_VOCABULARY.get(theme.lower(), [])
