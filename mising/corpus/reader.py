"""
Corpus reader and document representation for Mising texts.
"""

import csv
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Union
from mising.tokenization import sent_tokenize, word_tokenize
from mising.unicode_utils import normalize_mising_text


@dataclass
class CorpusDocument:
    """
    Represents a single document within a Mising language corpus.
    """
    id: str
    title: str
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    _sentences: Optional[List[str]] = field(default=None, repr=False)
    _tokens: Optional[List[str]] = field(default=None, repr=False)

    def __post_init__(self):
        self.text = normalize_mising_text(self.text)

    @property
    def sentences(self) -> List[str]:
        if self._sentences is None:
            self._sentences = sent_tokenize(self.text)
        return self._sentences

    @property
    def tokens(self) -> List[str]:
        if self._tokens is None:
            self._tokens = word_tokenize(self.text)
        return self._tokens

    @property
    def word_count(self) -> int:
        return len(self.tokens)

    @property
    def sentence_count(self) -> int:
        return len(self.sentences)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "text": self.text,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CorpusDocument":
        return cls(
            id=data.get("id", ""),
            title=data.get("title", "Untitled"),
            text=data.get("text", ""),
            metadata=data.get("metadata", {}),
        )


class CorpusReader:
    """
    Utility class to load documents from various formats (directory, JSONL, JSON, CSV).
    """

    @staticmethod
    def from_file(filepath: Union[str, Path], metadata: Optional[Dict[str, Any]] = None) -> CorpusDocument:
        path = Path(filepath)
        with path.open("r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        return CorpusDocument(
            id=path.stem,
            title=path.stem.replace("_", " ").title(),
            text=content,
            metadata=metadata or {"filename": path.name},
        )

    @staticmethod
    def from_directory(dirpath: Union[str, Path], glob_pattern: str = "*.txt") -> List[CorpusDocument]:
        directory = Path(dirpath)
        docs = []
        for file in sorted(directory.glob(glob_pattern)):
            if file.is_file():
                docs.append(CorpusReader.from_file(file))
        return docs

    @staticmethod
    def from_jsonl(filepath: Union[str, Path]) -> List[CorpusDocument]:
        path = Path(filepath)
        docs = []
        with path.open("r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if line:
                    data = json.loads(line)
                    docs.append(CorpusDocument.from_dict(data))
        return docs

    @staticmethod
    def to_jsonl(documents: List[CorpusDocument], filepath: Union[str, Path]) -> None:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            for doc in documents:
                f.write(json.dumps(doc.to_dict(), ensure_ascii=False) + "\n")

    @staticmethod
    def from_csv(filepath: Union[str, Path], text_col: str = "text", id_col: str = "id", title_col: str = "title") -> List[CorpusDocument]:
        path = Path(filepath)
        docs = []
        with path.open("r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                text = row.get(text_col, "")
                doc_id = row.get(id_col, f"doc_{i}")
                title = row.get(title_col, f"Document {i}")
                meta = {k: v for k, v in row.items() if k not in (text_col, id_col, title_col)}
                docs.append(CorpusDocument(id=doc_id, title=title, text=text, metadata=meta))
        return docs
