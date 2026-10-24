"""
Corpus Manager for indexing, searching, and querying Mising text collections.
"""

import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union
from mising.corpus.reader import CorpusDocument, CorpusReader
from mising.corpus.stats import FreqDist, compute_ngrams
from mising.tokenization import word_tokenize
from mising.unicode_utils import normalize_mising_text


@dataclass
class ConcordanceLine:
    """
    Key Word In Context (KWIC) search result.
    """
    doc_id: str
    doc_title: str
    sentence_idx: int
    left_context: str
    match: str
    right_context: str

    def format(self, left_width: int = 30, right_width: int = 30) -> str:
        """Format the concordance line with aligned columns."""
        left = self.left_context[-left_width:] if len(self.left_context) > left_width else self.left_context
        right = self.right_context[:right_width]
        return f"{self.doc_id:<10} | {left:>{left_width}} [{self.match}] {right:<{right_width}}"


class CorpusManager:
    """
    High-level manager for Mising text corpora.

    Provides indexed storage, concordance (KWIC) search, regex matching,
    metadata filtering, and statistical analysis.
    """

    def __init__(self, documents: Optional[List[CorpusDocument]] = None):
        self._documents: Dict[str, CorpusDocument] = {}
        if documents:
            for doc in documents:
                self.add_document(doc)

    def add_document(self, document: CorpusDocument) -> None:
        """Add a document to the corpus."""
        self._documents[document.id] = document

    def add_text(
        self,
        text: str,
        title: str = "Untitled",
        doc_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> CorpusDocument:
        """Create and add a new document from raw text."""
        id_str = doc_id or f"doc_{len(self._documents) + 1}"
        doc = CorpusDocument(
            id=id_str,
            title=title,
            text=text,
            metadata=metadata or {},
        )
        self.add_document(doc)
        return doc

    def get_document(self, doc_id: str) -> Optional[CorpusDocument]:
        return self._documents.get(doc_id)

    @property
    def documents(self) -> List[CorpusDocument]:
        return list(self._documents.values())

    def __len__(self) -> int:
        return len(self._documents)

    def __iter__(self) -> Iterable[CorpusDocument]:
        return iter(self._documents.values())

    def all_tokens(self, lower: bool = False) -> List[str]:
        """Aggregate tokens from all documents in the corpus."""
        tokens = []
        for doc in self._documents.values():
            if lower:
                tokens.extend([t.lower() for t in doc.tokens])
            else:
                tokens.extend(doc.tokens)
        return tokens

    def vocabulary(self, lower: bool = True) -> FreqDist:
        """Compute frequency distribution of all word tokens."""
        return FreqDist(self.all_tokens(lower=lower))

    def ngrams(self, n: int = 2, lower: bool = True) -> FreqDist:
        """Compute frequency distribution of N-grams across the corpus."""
        tokens = self.all_tokens(lower=lower)
        # Filter out standalone punctuation for cleaner lexical n-grams
        words_only = [t for t in tokens if any(c.isalnum() for c in t)]
        return FreqDist(compute_ngrams(words_only, n=n))

    def concordance(
        self,
        query: str,
        window: int = 5,
        case_sensitive: bool = False
    ) -> List[ConcordanceLine]:
        """
        Find all Key Word In Context (KWIC) occurrences of a word or phrase.

        Args:
            query: Word to search for.
            window: Number of words of context on the left and right.
            case_sensitive: Whether to match exact casing.

        Returns:
            List of ConcordanceLine instances.
        """
        results: List[ConcordanceLine] = []
        query_norm = normalize_mising_text(query)
        target = query_norm if case_sensitive else query_norm.lower()

        for doc in self._documents.values():
            for s_idx, sentence in enumerate(doc.sentences):
                tokens = word_tokenize(sentence)
                for i, tok in enumerate(tokens):
                    tok_comp = tok if case_sensitive else tok.lower()
                    if tok_comp == target:
                        left_tokens = tokens[max(0, i - window) : i]
                        right_tokens = tokens[i + 1 : min(len(tokens), i + 1 + window)]
                        results.append(
                            ConcordanceLine(
                                doc_id=doc.id,
                                doc_title=doc.title,
                                sentence_idx=s_idx,
                                left_context=" ".join(left_tokens),
                                match=tok,
                                right_context=" ".join(right_tokens),
                            )
                        )

        return results

    def search_regex(
        self,
        pattern: str,
        flags: int = re.IGNORECASE
    ) -> List[Tuple[CorpusDocument, int, str]]:
        """
        Search sentences matching a regular expression pattern across all documents.

        Args:
            pattern: Regular expression pattern string.
            flags: Regex flags (default re.IGNORECASE).

        Returns:
            List of (CorpusDocument, sentence_index, sentence_text) tuples.
        """
        compiled = re.compile(pattern, flags)
        matches: List[Tuple[CorpusDocument, int, str]] = []

        for doc in self._documents.values():
            for s_idx, sentence in enumerate(doc.sentences):
                if compiled.search(sentence):
                    matches.append((doc, s_idx, sentence))

        return matches

    def filter(self, **criteria) -> List[CorpusDocument]:
        """
        Filter documents by metadata attributes.

        Examples:
            >>> corpus.filter(genre="folklore", region="Majuli")
        """
        matching = []
        for doc in self._documents.values():
            match = True
            for k, v in criteria.items():
                if doc.metadata.get(k) != v:
                    match = False
                    break
            if match:
                matching.append(doc)
        return matching

    def stats(self) -> Dict[str, Any]:
        """Compute high-level corpus statistics."""
        docs = list(self._documents.values())
        total_sents = sum(doc.sentence_count for doc in docs)
        total_tokens = sum(doc.word_count for doc in docs)
        vocab = self.vocabulary(lower=True)

        return {
            "document_count": len(docs),
            "sentence_count": total_sents,
            "total_tokens": total_tokens,
            "unique_words": vocab.unique_types,
            "type_token_ratio": round(vocab.type_token_ratio, 4),
            "hapax_count": len(vocab.hapaxes()),
        }
