from mintrag.application.ports import Chunker, DocumentLoader
from mintrag.models.ingestion import Document, IngestionResult


class Ingestion:
    def __init__(self, loader: DocumentLoader, chunker: Chunker) -> None:
        self.loader = loader
        self.chunker = chunker

    def ingest(self, source: str) -> IngestionResult:
        document: Document = self.loader.load(source)
        splitResult = self.chunker.split(document=document)

        if isinstance(splitResult, Document):
            document = splitResult
            chunks = document.chunks or ()
        else:
            chunks = tuple(splitResult)
            document.chunks = chunks

        return IngestionResult(document=document, chunks=chunks)
