"""
Tests for Unicode normalization and file utilities.
"""

import tempfile
from pathlib import Path
import pytest
from mising.unicode_utils import (
    normalize_mising_text,
    detect_script,
    is_mising_character,
    read_mising_file,
    write_mising_file,
    clean_text,
)


def test_unicode_normalization_combining_accents():
    # 'e' + combining acute (U+0301) should normalize to precomposed 'é' (U+00E9)
    decomposed_e = "e\u0301"
    decomposed_i = "i\u0301"
    normalized_e = normalize_mising_text(decomposed_e)
    normalized_i = normalize_mising_text(decomposed_i)

    assert normalized_e == "é"
    assert normalized_i == "í"


def test_unicode_normalization_variants():
    # Legacy IPA schwa or barred-i variants
    text = "ami-k\u0268d\u0268-lo g\u0259rdu\u014b"
    norm = normalize_mising_text(text)
    assert "í" in norm
    assert "é" in norm


def test_punctuation_and_quote_normalization():
    raw = "‘Mising’ – agom “kampo”"
    norm = normalize_mising_text(raw)
    assert norm == "'Mising' - agom \"kampo\""


def test_detect_script():
    latin_sample = "Ngo Mising agom kénam ami."
    assamese_sample = "ঙম মিচিং আগম কীনাম অমি।"
    mixed_sample = "Ngo Mising অমি।"

    assert detect_script(latin_sample) == "latin"
    assert detect_script(assamese_sample) == "assamese"
    assert detect_script(mixed_sample) == "mixed"
    assert detect_script("12345 !@#$") == "unknown"


def test_is_mising_character():
    assert is_mising_character("a") is True
    assert is_mising_character("é") is True
    assert is_mising_character("í") is True
    assert is_mising_character("k") is True
    assert is_mising_character("ŋ") is True
    assert is_mising_character("x") is False
    assert is_mising_character("z") is False
    assert is_mising_character("long") is False


def test_clean_text():
    dirty = "  Ngo giduŋ.  \n\n\n   No inlang.   "
    cleaned = clean_text(dirty)
    assert cleaned == "Ngo giduŋ.\nNo inlang."


def test_file_io_roundtrip():
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test_mising.txt"
        original_text = "Ngo Mising agom kénam ami.\nAli-Aye-Ligang botteba lígango."

        write_mising_file(test_file, original_text)
        assert test_file.exists()

        loaded_text = read_mising_file(test_file)
        assert loaded_text == original_text
