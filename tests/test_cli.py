"""
Tests for the Command-Line Interface (CLI).
"""

import sys
from io import StringIO
import pytest
from mising.cli import main


def test_cli_tokenize(capsys):
    main(["tokenize", "Ngo", "giduŋ."])
    captured = capsys.readouterr().out
    assert "Sentences" in captured
    assert "Tokens" in captured


def test_cli_tag(capsys):
    main(["tag", "Ngo", "okumlo", "giduŋ."])
    captured = capsys.readouterr().out
    assert "PRON" in captured
    assert "VERB" in captured


def test_cli_stem(capsys):
    main(["stem", "ami-kídí-lo"])
    captured = capsys.readouterr().out
    assert "ami" in captured


def test_cli_analyze(capsys):
    main(["analyze", "ger-duŋ-ma"])
    captured = capsys.readouterr().out
    assert "Root: ger" in captured
    assert "CONT" in captured


def test_cli_transliterate(capsys):
    main(["transliterate", "Mising", "--target", "assamese"])
    captured = capsys.readouterr().out
    assert "মি" in captured and any(sub in captured for sub in ["চিং", "সিং", "চিঙ", "সিঙ"])


def test_cli_number(capsys):
    main(["number", "15", "--noun", "ami"])
    captured = capsys.readouterr().out
    assert "iing-ango" in captured
    assert "ami gor-iing-ango" in captured


def test_cli_dict(capsys):
    main(["dict", "okum"])
    captured = capsys.readouterr().out
    assert "house" in captured.lower()
