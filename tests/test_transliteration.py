"""
Tests for transliteration across Mising Latin, Assamese script, ASCII, and IPA.
"""

from mising.transliteration import (
    mising_to_assamese,
    assamese_to_mising,
    mising_to_ipa,
    mising_to_ascii,
    ascii_to_mising,
    transliterate,
)


def test_mising_to_assamese():
    res = mising_to_assamese("Mising")
    assert "মি" in res
    assert any(sub in res for sub in ["চিং", "সিং", "চিঙ", "সিঙ"])


def test_mising_central_vowels_to_assamese():
    # 'é' (/ə/) and 'í' (/ɨ/) should map with diacritic markers in Assamese
    res_e = mising_to_assamese("kénam")
    res_i = mising_to_assamese("kídí")
    assert "কে'" in res_e or "ে'" in res_e
    assert "কি'" in res_i or "ি'" in res_i


def test_assamese_to_mising():
    # Reverse conversion
    res = assamese_to_mising("মিচিং")
    assert "mic" in res or "mis" in res


def test_mising_to_ipa():
    # 'apong' -> /apoŋ/
    ipa = mising_to_ipa("apong")
    assert ipa == "apoŋ"

    # 'ami-kídí' -> /ami-kɨdi/
    ipa_vowels = mising_to_ipa("kídí")
    assert "ɨ" in ipa_vowels


def test_mising_to_ascii_roundtrip():
    original = "ami-kídí-lo kénam"
    ascii_rep = mising_to_ascii(original)
    assert "ki'di'" in ascii_rep
    assert "ke'nam" in ascii_rep

    restored = ascii_to_mising(ascii_rep)
    assert restored == original


def test_transliterate_dispatcher():
    res1 = transliterate("apong", source="mising", target="ipa")
    assert res1 == "apoŋ"

    res2 = transliterate("apong", source="mising", target="ascii")
    assert res2 == "apong"
