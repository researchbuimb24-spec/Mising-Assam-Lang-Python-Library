"""
Statistical distribution and N-gram utilities for Mising corpus analysis.
"""

from collections import Counter
from typing import Any, Dict, Iterable, List, Optional, Tuple


def compute_ngrams(tokens: List[str], n: int = 2) -> List[Tuple[str, ...]]:
    """
    Generate N-grams from a sequence of tokens.

    Args:
        tokens: Sequence of token strings.
        n: N-gram length (e.g. 2 for bigrams, 3 for trigrams).

    Returns:
        List of n-gram tuples.

    Examples:
        >>> compute_ngrams(['ngo', 'mising', 'agom', 'kénam'], n=2)
        [('ngo', 'mising'), ('mising', 'agom'), ('agom', 'kénam')]
    """
    if n < 1:
        raise ValueError("n must be at least 1")
    if len(tokens) < n:
        return []
    return [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


class FreqDist:
    """
    Frequency distribution for tokens, stems, or N-grams in a Mising corpus.
    """

    def __init__(self, samples: Optional[Iterable] = None):
        self._counter: Counter = Counter()
        if samples:
            self._counter.update(samples)

    def update(self, samples: Iterable) -> None:
        self._counter.update(samples)

    def __getitem__(self, item) -> int:
        return self._counter[item]

    def __len__(self) -> int:
        return len(self._counter)

    def __iter__(self):
        return iter(self._counter)

    def __contains__(self, item) -> bool:
        return item in self._counter

    @property
    def total_tokens(self) -> int:
        """Total number of sample instances counted (N)."""
        return sum(self._counter.values())

    @property
    def unique_types(self) -> int:
        """Number of distinct unique types / vocabulary size (V or B)."""
        return len(self._counter)

    @property
    def type_token_ratio(self) -> float:
        """
        Lexical diversity metric: Types / Tokens (TTR).
        Returns a float between 0.0 and 1.0.
        """
        n = self.total_tokens
        if n == 0:
            return 0.0
        return self.unique_types / n

    def freq(self, item) -> float:
        """Calculate the relative frequency (probability) of an item."""
        n = self.total_tokens
        if n == 0:
            return 0.0
        return self._counter[item] / n

    def most_common(self, n: Optional[int] = None) -> List[Tuple[Any, int]]:
        """Return the n most frequent items and their counts."""
        return self._counter.most_common(n)

    def hapaxes(self) -> List[Any]:
        """Return list of items that occur exactly once (hapax legomena)."""
        return [item for item, count in self._counter.items() if count == 1]

    def ascii_chart(self, top_n: int = 10, max_width: int = 40) -> str:
        """
        Generate a visual ASCII bar chart of the top N most frequent items.
        """
        top_items = self.most_common(top_n)
        if not top_items:
            return "No frequency data available."

        max_count = top_items[0][1]
        max_label_len = max(len(str(item)) for item, _ in top_items)

        lines = [f"{'Item':<{max_label_len}} | {'Count':<5} | Bar"]
        lines.append("-" * (max_label_len + 15 + max_width))

        for item, count in top_items:
            bar_len = int((count / max_count) * max_width) if max_count > 0 else 0
            bar = "█" * bar_len
            lines.append(f"{str(item):<{max_label_len}} | {count:<5} | {bar}")

        return "\n".join(lines)
