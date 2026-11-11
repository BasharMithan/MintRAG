from mintrag.application.ports import Chunker, DocumentLoader
from mintrag.models.ingestion import Chunk, Document, IngestionResult


class Ingestion:
    def __init__(self, loader: DocumentLoader, chunker: Chunker) -> None:
        self.loader = loader
        self.chunker = chunker



    def ingest(self, source: str) -> IngestionResult:
        document: Document = self.loader.load(source)
        chunks: tuple[Chunk, ...] = self.chunker.split(document=document)
        return IngestionResult(document=document, chunks=chunks)
