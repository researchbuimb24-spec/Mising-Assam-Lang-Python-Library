"""
Part-of-speech (POS) tagging for the Mising language.

Provides rule-based, dictionary-backed, and statistical taggers for Mising text.
"""

from mising.pos.tagger import MisingPOSTagger, pos_tag

__all__ = ["MisingPOSTagger", "pos_tag"]
