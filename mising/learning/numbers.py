"""
Numeral generation and noun classification system for the Mising language.

Mising has a rich vigesimal/decimal counting system and an obligatory
classifier system where counting nouns requires a specific numeral classifier
(e.g., 'gor' for humans, 'abor' for animals, 'bar' for flat objects).
"""

from typing import Dict, Optional, Tuple


CARDINAL_DIGITS: Dict[int, str] = {
    0: "tílo",
    1: "ako",
    2: "anyi",
    3: "aum",
    4: "api",
    5: "ango",
    6: "akké",
    7: "kinid",
    8: "pini",
    9: "konang",
    10: "iing",
}

TENS_MULTIPLES: Dict[int, str] = {
    10: "iing",
    20: "nyiing",
    30: "umiing",
    40: "píyiing",
    50: "ngoyiing",
    60: "kíyiing",
    70: "kindiing",
    80: "piniing",
    90: "konyiing",
}

# Standard Numeral Classifiers and their target semantic categories
CLASSIFIERS_DATA: Dict[str, Dict[str, str]] = {
    "gor": {
        "category": "Human beings",
        "description": "Used for people, men, women, children (e.g. ami gor-ako)",
        "example_noun": "ami",
    },
    "abor": {
        "category": "Animals / Beasts",
        "description": "Used for four-legged animals, birds, fish (e.g. ékké abor-anyi)",
        "example_noun": "ékké",
    },
    "bor": {
        "category": "Trees / Long standing plants",
        "description": "Used for trees, bamboo, trunks (e.g. asom bor-ako)",
        "example_noun": "asom",
    },
    "bar": {
        "category": "Flat flexible items",
        "description": "Used for cloths, blankets, woven mats (e.g. égé bar-ako)",
        "example_noun": "égé",
    },
    "kol": {
        "category": "Round objects / Fruits",
        "description": "Used for fruits, balls, round items (e.g. aye kol-ako)",
        "example_noun": "aye",
    },
    "pat": {
        "category": "Leaves / Sheets of paper",
        "description": "Used for tree leaves, flat sheets (e.g. kopat pat-ako)",
        "example_noun": "kopat",
    },
    "pum": {
        "category": "Households / Bundles",
        "description": "Used for houses, families, bound bundles (e.g. okum pum-ako)",
        "example_noun": "okum",
    },
}

# Common noun to default classifier mapping
DEFAULT_NOUN_CLASSIFIERS: Dict[str, str] = {
    "ami": "gor",
    "mising": "gor",
    "ao": "gor",
    "omé": "gor",
    "abu": "gor",
    "ane": "gor",
    "babu": "gor",
    "biro": "gor",
    "sine": "abor",
    "simyo": "abor",
    "ékké": "abor",
    "ekke": "abor",
    "ményo": "abor",
    "sho": "abor",
    "ég": "abor",
    "poro": "abor",
    "péttang": "abor",
    "éngo": "abor",
    "asom": "bor",
    "aye": "kol",
    "okum": "pum",
}


def number_to_mising(n: int) -> str:
    """
    Convert an integer (0 to 999) to its Mising numeral word.

    Args:
        n: Non-negative integer.

    Returns:
        Mising numeral string.

    Examples:
        >>> number_to_mising(1)
        'ako'
        >>> number_to_mising(15)
        'iing-ango'
        >>> number_to_mising(20)
        'nyiing'
        >>> number_to_mising(23)
        'nyiing-aum'
        >>> number_to_mising(100)
        'lingko'
    """
    if n < 0:
        raise ValueError("Only non-negative integers are supported.")

    if n in CARDINAL_DIGITS:
        return CARDINAL_DIGITS[n]

    if 11 <= n <= 19:
        unit = n % 10
        return f"iing-{CARDINAL_DIGITS[unit]}"

    if 20 <= n <= 99:
        tens = (n // 10) * 10
        remainder = n % 10
        tens_str = TENS_MULTIPLES[tens]
        if remainder == 0:
            return tens_str
        return f"{tens_str}-{CARDINAL_DIGITS[remainder]}"

    if n == 100:
        return "lingko"

    if 101 <= n <= 999:
        hundreds = n // 100
        rem = n % 100
        if hundreds == 1:
            h_str = "lingko"
        else:
            h_str = f"ling-{CARDINAL_DIGITS[hundreds]}"

        if rem == 0:
            return h_str
        return f"{h_str} {number_to_mising(rem)}"

    return str(n)


def classified_noun(noun: str, count: int, classifier: Optional[str] = None) -> str:
    """
    Generate a grammatically correct Mising counted noun phrase with its numeral classifier.

    In Mising, counting follows the structure:
        [Noun] + [Classifier]-[Numeral]
    For example:
        'ami gor-ako' (one person)
        'sine abor-anyi' (two elephants)
        'okum pum-aum' (three houses)

    Args:
        noun: The noun to count (e.g. 'ami', 'ékké', 'okum').
        count: The number count (1, 2, 3...).
        classifier: Optional explicit classifier. If omitted, the default classifier
                    for known nouns is automatically looked up.

    Returns:
        Formatted counted phrase string.

    Examples:
        >>> classified_noun("ami", 1)
        'ami gor-ako'
        >>> classified_noun("sine", 2)
        'sine abor-anyi'
        >>> classified_noun("okum", 3, classifier="pum")
        'okum pum-aum'
    """
    clf = classifier
    if not clf:
        clf = DEFAULT_NOUN_CLASSIFIERS.get(noun.lower(), "gor")

    num_word = number_to_mising(count)
    return f"{noun} {clf}-{num_word}"
