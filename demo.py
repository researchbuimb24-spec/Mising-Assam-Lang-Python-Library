"""
demo.py - Example of using the Mising library in a Python program.
"""

import sys
import mising

# Ensure UTF-8 output display in Windows terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main():
    print("=== MISING NLP LIBRARY IN PYTHON ===\n")

    # 1. SAMPLE INPUT TEXT
    text = "Ngo Mising agom kénam ami. No kolo giduŋ? Ngo okum-lo yarto।"
    print(f"Original Text:\n  {text}\n")

    # 2. SENTENCE & WORD TOKENIZATION
    sentences = mising.sent_tokenize(text)
    print(f"1. Sentences ({len(sentences)}):")
    for i, sent in enumerate(sentences, 1):
        words = mising.word_tokenize(sent)
        print(f"   [{i}] {sent}")
        print(f"       Words: {words}")
    print()

    # 3. PART-OF-SPEECH (POS) TAGGING
    sample_sentence = "Ngo okum-lo giduŋ."
    tagged = mising.pos_tag(sample_sentence)
    print(f"2. POS Tagging for '{sample_sentence}':")
    for word, tag in tagged:
        print(f"   {word:<12} -> {tag}")
    print()

    # 4. STEMMING & MORPHOLOGICAL ANALYSIS
    word = "ami-kídí-lo"
    stem = mising.stem(word)
    analysis = mising.analyze(word)
    print(f"3. Morphological Analysis for '{word}':")
    print(f"   Root Stem:  {stem}")
    print(f"   Gloss:      {analysis.gloss}")
    print(f"   Features:   {analysis.features}\n")

    # 5. TRANSLITERATION (Roman <-> Assamese Script <-> IPA)
    mising_phrase = "Ali-Aye-Ligang botteba lígango."
    as_script = mising.transliterate(mising_phrase, source="mising", target="assamese")
    ipa = mising.transliterate(mising_phrase, source="mising", target="ipa")
    print("4. Transliteration:")
    print(f"   Roman:      {mising_phrase}")
    print(f"   Assamese:   {as_script}")
    print(f"   IPA:        /{ipa}/\n")

    # 6. NUMBERS & NOUN CLASSIFIERS
    count = 15
    mising_num = mising.number_to_mising(count)
    phrase = mising.classified_noun("ami", count)
    print("5. Numbers & Classifiers:")
    print(f"   Count {count} in Mising: {mising_num}")
    print(f"   Counted phrase:        {phrase} (15 persons)\n")

    # 7. DICTIONARY LOOKUP
    entry = mising.lookup("okum")
    if entry:
        print(f"6. Dictionary Entry for '{entry.mising}':")
        print(f"   POS:        {entry.pos}")
        print(f"   English:    {entry.english}")
        print(f"   Assamese:   {entry.assamese}")
        print(f"   IPA:        /{entry.ipa}/")


if __name__ == "__main__":
    main()
