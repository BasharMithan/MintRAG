from mintrag.models.ingestion import Chunk as Chunk
from mintrag.models.ingestion import Document as Document
from mintrag.models.ingestion import IngestionResult as IngestionResult

__all__ = ["Chunk", "Document", "IngestionResult"]


def main() -> None:
    from mintrag.main import main as run

    run()
