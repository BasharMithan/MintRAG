from pathlib import Path
from mintrag.domain.models.ingestion import Document, Chunk, IngestionResult
from mintrag.application.ports import DocumentLoader, Chunker


class Ingestion:
    def __init__(self, loader: DocumentLoader, chunker: Chunker) -> None:
        self.loader = loader
        self.chunker = chunker



    def ingest(self, source: str) -> IngestionResult:
        document: Document = self.loader.load(source)
        chunks: tuple[Chunk, ...] = self.chunker.split(document=document)
        return IngestionResult(document=document, chunks=chunks)

