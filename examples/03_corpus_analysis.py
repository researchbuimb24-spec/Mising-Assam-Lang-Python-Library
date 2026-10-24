"""
03_corpus_analysis.py - Corpus Management, Search, and Statistical Analysis.
"""

import sys
import mising

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

def main():
    print("=" * 60)
    print("  Mising Corpus Management & Linguistic Search")
    print("=" * 60)

    # 1. Load Built-in Authenticated Sample Corpus
    corpus = mising.load_sample_corpus()
    stats = corpus.stats()
    print("\n1. Corpus Overview:")
    for metric, val in stats.items():
        print(f"   {metric.replace('_', ' ').title():<22}: {val}")

    # 2. Key Word In Context (KWIC) / Concordance Search
    query = "agom"
    print(f"\n2. Concordance Search for '{query}':")
    matches = corpus.concordance(query, window=4)
    for m in matches:
        print(f"   {m.format(left_width=25, right_width=25)}")

    # 3. Regular Expression Search (e.g. Find all sentences with continuous verbs -duŋ)
    pattern = r"\b\w+duŋ\b"
    print(f"\n3. Regex Pattern Search for '{pattern}':")
    regex_matches = corpus.search_regex(pattern)
    for doc, s_idx, sent in regex_matches[:3]:
        print(f"   [{doc.id}] Line {s_idx + 1}: {sent}")

    # 4. Frequency Distribution & Top Vocabulary
    vocab = corpus.vocabulary(lower=True)
    print(f"\n4. Top 10 Most Frequent Words:")
    print(vocab.ascii_chart(top_n=10, max_width=30))

    # 5. N-gram Collocations (Bigrams)
    print("\n5. Top 5 Bigrams in Corpus:")
    bigrams_dist = corpus.ngrams(n=2, lower=True)
    for bg, count in bigrams_dist.most_common(5):
        print(f"   {' '.join(bg):<25} : {count} occurrences")

if __name__ == "__main__":
    main()
