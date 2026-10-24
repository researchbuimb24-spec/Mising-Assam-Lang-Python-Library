"""
Command-Line Interface for the Mising NLP Library.
"""

import argparse
import sys
from typing import List, Optional
import mising

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def print_banner():
    banner = f"""
======================================================
  Mising NLP Toolkit v{mising.__version__}
  Computational Linguistics for the Mising Language
======================================================
"""
    print(banner)


def cmd_tokenize(args):
    text = " ".join(args.text)
    print(f"Input: {text}\n")
    sentences = mising.sent_tokenize(text)
    print(f"Sentences ({len(sentences)}):")
    for i, s in enumerate(sentences, 1):
        words = mising.word_tokenize(s)
        print(f"  [{i}] {s}")
        print(f"      Tokens ({len(words)}): {words}")


def cmd_tag(args):
    text = " ".join(args.text)
    print(f"Input: {text}\n")
    tagged = mising.pos_tag(text)
    print(f"{'Token':<20} | {'POS Tag':<10}")
    print("-" * 35)
    for tok, tag in tagged:
        print(f"{tok:<20} | {tag:<10}")


def cmd_stem(args):
    word = args.word
    stemmed = mising.stem(word)
    print(f"Word:    {word}")
    print(f"Stem:    {stemmed}")


def cmd_analyze(args):
    word = args.word
    res = mising.analyze(word)
    print(res.summary())
    print(f"Interlinear Gloss: {res.gloss}")


def cmd_transliterate(args):
    text = " ".join(args.text)
    result = mising.transliterate(text, source=args.source, target=args.target)
    print(f"Source ({args.source}): {text}")
    print(f"Target ({args.target}): {result}")


def cmd_number(args):
    num = args.number
    word = mising.number_to_mising(num)
    print(f"Number:  {num}")
    print(f"Mising:  {word}")
    if args.noun:
        phrase = mising.classified_noun(args.noun, num, classifier=args.classifier)
        print(f"Phrase:  {phrase}")


def cmd_dict(args):
    query = args.query
    entry = mising.lookup(query)
    if entry:
        print(f"\n[{entry.mising.upper()}] ({entry.pos})")
        print(f"  English:  {entry.english}")
        print(f"  Assamese: {entry.assamese}")
        if entry.ipa:
            print(f"  IPA:      /{entry.ipa}/")
        if entry.examples:
            print("  Examples:")
            for ex in entry.examples:
                print(f"    • {ex.get('mising', '')} -> {ex.get('english', '')}")
    else:
        # Try search in english
        d = mising.get_default_dictionary()
        matches = d.search_english(query)
        if matches:
            print(f"\nFound {len(matches)} matching entries for '{query}':")
            for m in matches:
                print(f"  • {m.mising} ({m.pos}): {m.english}")
        else:
            print(f"No entry found for '{query}'.")


def cmd_corpus(args):
    corpus = mising.load_sample_corpus()
    if args.subcommand == "stats":
        stats = corpus.stats()
        print("\n--- Mising Sample Corpus Statistics ---")
        for k, v in stats.items():
            print(f"  {k.replace('_', ' ').title():<22}: {v}")
        print("\nTop 10 Vocabulary Words:")
        print(corpus.vocabulary().ascii_chart(top_n=10))

    elif args.subcommand == "concordance":
        query = args.query
        lines = corpus.concordance(query)
        print(f"\nConcordance for '{query}' ({len(lines)} matches):")
        for line in lines:
            print(line.format())


def cmd_quiz(args):
    deck = mising.create_deck(theme=args.theme)
    quiz = deck.generate_quiz(num_questions=args.count)
    if not quiz:
        print("No questions could be generated.")
        return

    print(f"\n--- Mising Language Quiz ({deck.name}) ---")
    score = 0
    for i, q in enumerate(quiz, 1):
        print(f"\nQ{i}. What does '{q.prompt}' mean? (/{q.ipa}/, Assamese: {q.assamese})")
        for opt_idx, opt in enumerate(q.options, 1):
            print(f"   [{opt_idx}] {opt}")

        while True:
            choice = input("\nYour answer (1-4, or 'q' to quit): ").strip()
            if choice.lower() == "q":
                print(f"Quiz aborted. Score: {score}/{i - 1}")
                return
            if choice in ("1", "2", "3", "4"):
                chosen_text = q.options[int(choice) - 1]
                if q.check(chosen_text):
                    print("✓ Correct!")
                    score += 1
                else:
                    print(f"✗ Incorrect. The right answer is: {q.correct_answer}")
                break
            else:
                print("Please enter a number between 1 and 4.")

    print(f"\nFinal Score: {score}/{len(quiz)} ({int((score / len(quiz)) * 100)}%)")


def main(argv: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(
        prog="mising",
        description="Mising Natural Language Processing Toolkit CLI",
    )
    parser.add_argument("--version", action="version", version=f"mising {mising.__version__}")
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # Tokenize
    p_tok = subparsers.add_parser("tokenize", help="Tokenize sentences and words")
    p_tok.add_argument("text", nargs="+", help="Text to tokenize")

    # Tag
    p_tag = subparsers.add_parser("tag", help="Part-of-Speech tagging")
    p_tag.add_argument("text", nargs="+", help="Text to POS tag")

    # Stem
    p_stem = subparsers.add_parser("stem", help="Stem a word")
    p_stem.add_argument("word", help="Word to stem")

    # Analyze
    p_ana = subparsers.add_parser("analyze", help="Morphological analysis of a word")
    p_ana.add_argument("word", help="Word to analyze")

    # Transliterate
    p_trans = subparsers.add_parser("transliterate", help="Transliterate between scripts")
    p_trans.add_argument("text", nargs="+", help="Text to transliterate")
    p_trans.add_argument("--source", default="mising", choices=["mising", "assamese", "ascii"], help="Source script")
    p_trans.add_argument("--target", default="assamese", choices=["assamese", "mising", "ipa", "ascii"], help="Target script")

    # Number
    p_num = subparsers.add_parser("number", help="Generate Mising number words and classified nouns")
    p_num.add_argument("number", type=int, help="Number to convert")
    p_num.add_argument("--noun", help="Optional noun to count")
    p_num.add_argument("--classifier", help="Optional classifier override")

    # Dict
    p_dict = subparsers.add_parser("dict", help="Search the Mising dictionary")
    p_dict.add_argument("query", help="Mising word or English keyword")

    # Corpus
    p_corp = subparsers.add_parser("corpus", help="Corpus tools")
    corp_sub = p_corp.add_subparsers(dest="subcommand", help="Corpus actions")
    p_cstats = corp_sub.add_parser("stats", help="Show corpus statistics")
    p_cconc = corp_sub.add_parser("concordance", help="Concordance search")
    p_cconc.add_argument("query", help="Word to search")

    # Quiz
    p_quiz = subparsers.add_parser("quiz", help="Interactive vocabulary quiz")
    p_quiz.add_argument("--theme", choices=mising.list_themes(), help="Optional theme filter")
    p_quiz.add_argument("--count", type=int, default=5, help="Number of questions (default 5)")

    args = parser.parse_args(argv)

    if not args.command:
        print_banner()
        parser.print_help()
        sys.exit(0)

    if args.command == "tokenize":
        cmd_tokenize(args)
    elif args.command == "tag":
        cmd_tag(args)
    elif args.command == "stem":
        cmd_stem(args)
    elif args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "transliterate":
        cmd_transliterate(args)
    elif args.command == "number":
        cmd_number(args)
    elif args.command == "dict":
        cmd_dict(args)
    elif args.command == "corpus":
        cmd_corpus(args)
    elif args.command == "quiz":
        cmd_quiz(args)


if __name__ == "__main__":
    main()
