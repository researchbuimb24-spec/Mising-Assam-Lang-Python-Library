import mising

# 1. Splitting text into sentences and words
text = "Ngo Mising agom kénam ami. No kolo giduŋ?"
sentences = mising.sent_tokenize(text)
words = mising.word_tokenize(sentences[0])
print("Sentences:", sentences)
print("Words:    ", words)

# 2. Part-of-Speech (POS) tagging
tagged = mising.pos_tag("Ngo okum-lo giduŋ.")
print("POS Tags: ", tagged)
# Output: [('Ngo', 'PRON'), ('okum-lo', 'NOUN'), ('giduŋ', 'VERB'), ('.', 'PUNCT')]

# 3. Stemming & morphological analysis
print("Stem:     ", mising.stem("ami-kídí-lo"))  # Output: 'ami'
analysis = mising.analyze("ami-kídí-lo")
print("Gloss:    ", analysis.gloss)              # Output: 'ami-PL-LOC'

# 4. Transliteration (Roman <-> Assamese Script <-> IPA)
as_script = mising.transliterate("Mising agom", target="assamese")
ipa = mising.transliterate("apong", target="ipa")
print("Assamese: ", as_script)  # Output: 'মিচিঙ্ আগোম্'
print("IPA:      ", ipa)        # Output: 'apoŋ'

# 5. Numerals & noun classifiers
number_word = mising.number_to_mising(15)        # Output: 'iing-ango'
person_count = mising.classified_noun("ami", 1)  # Output: 'ami gor-ako'
print("15 in Mising:", number_word)
print("1 person:    ", person_count)

# 6. Dictionary lookup
entry = mising.lookup("okum")
if entry:
    print(f"Dictionary '{entry.mising}': {entry.english} ({entry.assamese})")
