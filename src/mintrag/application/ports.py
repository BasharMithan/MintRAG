from typing import Protocol

import numpy as np

from mintrag.models import Chunk, Document


class DocumentLoader(Protocol):
    def load(self, source: str) -> Document:
        """Loads a non-empty document or raise an error."""
        ...


class Chunker(Protocol):
    def split(self, document: Document) -> tuple[Chunk, ...]:
        "Returns orderd chunks with offsets into the document text."
        ...


class Embedder(Protocol):
    dimentions: int

    def embeddDocument(
        self, document: Document
    ) -> Document: ...  # Shape (n, dimension)
    def embeddQuery(self, text: str) -> np.ndarray: ...  # Shape (dimension, n)


class VectorStore(Protocol):
    def add(self, chunks: list[Chunk], vectors: np.ndarray) -> None: ...
    def search(
        self, queryVector: np.ndarray, k: int
    ) -> list: ...  # list[RetrievalChunk]
    def deteleDocument(self, documentID: int) -> bool: ...

    def hasDocument(self, documentID: int) -> bool: ...
    def listDcouments(self) -> list[Document]: ...
    def count(self) -> int: ...
    def save(self) -> None: ...
    def load(self) -> None: ...
