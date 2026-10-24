"""
02_transliteration_demo.py - Multi-Script Transliteration for Mising.
"""

import sys
import mising

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

def main():
    print("=" * 60)
    print("  Mising Script Transliteration Demonstration")
    print("=" * 60)

    phrases = [
        "Mising agom",
        "Ali-Aye-Ligang botteba lígango.",
        "Ami-kídí apong tila Gumrag sokiduŋ.",
        "Doolung bottepe bírma, ami kampope bírduŋ.",
    ]

    for p in phrases:
        print(f"\nOriginal (MAK Roman):    {p}")
        
        # 1. To Assamese Script
        assamese_text = mising.transliterate(p, source="mising", target="assamese")
        print(f"Assamese Script:         {assamese_text}")

        # 2. To International Phonetic Alphabet (IPA)
        ipa_text = mising.transliterate(p, source="mising", target="ipa")
        print(f"Phonetic (IPA):          /{ipa_text}/")

        # 3. To Simplified ASCII (diacritic-free)
        ascii_text = mising.transliterate(p, source="mising", target="ascii")
        print(f"Simplified ASCII:        {ascii_text}")

    # Bidirectional Roundtrip
    print("\n" + "-" * 50)
    print("Bidirectional Conversion Test:")
    orig = "ami-kídí-lo"
    as_script = mising.mising_to_assamese(orig)
    print(f"  Roman -> Assamese:  {orig} -> {as_script}")

    ascii_form = mising.mising_to_ascii(orig)
    restored = mising.ascii_to_mising(ascii_form)
    print(f"  Roman -> ASCII:     {orig} -> {ascii_form}")
    print(f"  ASCII -> Restored:  {ascii_form} -> {restored}")
    assert restored == orig
    print("  ✓ Full fidelity roundtrip successful!")

if __name__ == "__main__":
    main()
