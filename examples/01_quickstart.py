"""
01_quickstart.py - Basic NLP Pipeline with the Mising library.
"""

import sys
import mising

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

def main():
    print("=" * 60)
    print("  Mising NLP Library - Quickstart Demonstration")
    print("=" * 60)

    # 1. Unicode Normalization & Script Detection
    raw_text = "‘Mising’ agom si Assam-lo kénam agom. No kolo giduŋ? Ngo okumlo yarto।  "
    normalized = mising.normalize_mising_text(raw_text)
    print(f"\n1. Normalization:\n   Raw:        {raw_text}\n   Normalized: {normalized}")
    print(f"   Script:     {mising.detect_script(normalized)}")

    # 2. Sentence Tokenization
    sentences = mising.sent_tokenize(normalized)
    print(f"\n2. Sentence Segmentation ({len(sentences)} sentences):")
    for i, s in enumerate(sentences, 1):
        print(f"   [{i}] {s}")

    # 3. Word Tokenization (with clitics and punctuation)
    sample_sent = "Ngo okum-lo giduŋ."
    tokens = mising.word_tokenize(sample_sent)
    print(f"\n3. Word Tokenization:\n   Sentence: {sample_sent}\n   Tokens:   {tokens}")

    # 4. Syllable and Character Tokenization
    word = "doolung"
    syllables = mising.syllable_tokenize(word)
    graphemes = mising.char_tokenize(word, group_digraphs=True)
    print(f"\n4. Sub-word Tokenization for '{word}':")
    print(f"   Syllables:  {syllables}")
    print(f"   Graphemes:  {graphemes}")

    # 5. Stemming & Morphological Analysis
    complex_word = "ami-kídí-lo"
    stem_result = mising.stem(complex_word)
    analysis = mising.analyze(complex_word)
    print(f"\n5. Morphological Analysis for '{complex_word}':")
    print(f"   Stem:       {stem_result}")
    print(f"   Gloss:      {analysis.gloss}")
    print(f"   Features:   {analysis.features}")

    # 6. Part-of-Speech (POS) Tagging
    tagged = mising.pos_tag(sample_sent)
    print(f"\n6. Part-of-Speech Tagging for '{sample_sent}':")
    for token, tag in tagged:
        print(f"   {token:<12} -> {tag}")

if __name__ == "__main__":
    main()
