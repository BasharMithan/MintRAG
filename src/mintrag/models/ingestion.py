from pydantic import BaseModel


class Chunk(BaseModel):
    id: str
    documentID: str
    text: str
    source: str
    index: int
    start: int
    end: int


class Document(BaseModel):
    id: str
    text: str
    source: str

    chunks: tuple[Chunk, ...] | None = None
    embeddings: tuple[tuple[float, ...], ...] | None = None


class IngestionResult(BaseModel):
    document: Document
    chunks: tuple[Chunk, ...]
