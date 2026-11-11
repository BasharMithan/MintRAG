from typing import Protocol

from mintrag.domain.models import Chunk, Document


class DocumentLoader(Protocol):
    def load(self, source: str) -> Document:
        """Loads a non-empty document or raise an error."""
        ...



class Chunker(Protocol):
    def split(self, document: Document) -> tuple[Chunk, ...]:
        "Returns orderd chunks with offsets into the document text."
        ...

