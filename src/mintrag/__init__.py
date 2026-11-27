from mintrag.customExceptions import (
    DocumentLoadError as DocumentLoadError,
)
from mintrag.customExceptions import (
    DocumentNotFoundError as DocumentNotFoundError,
)
from mintrag.customExceptions import (
    EmbeddingError as EmbeddingError,
)
from mintrag.customExceptions import (
    EmptyDocumentError as EmptyDocumentError,
)
from mintrag.customExceptions import (
    InvalidQueryError as InvalidQueryError,
)
from mintrag.customExceptions import (
    MintRAGError as MintRAGError,
)
from mintrag.customExceptions import (
    UnsupportedDocumentTypeError as UnsupportedDocumentTypeError,
)
from mintrag.models.ingestion import Chunk as Chunk
from mintrag.models.ingestion import Document as Document
from mintrag.models.ingestion import IngestionResult as IngestionResult

__all__ = [
    "Chunk",
    "Document",
    "DocumentLoadError",
    "DocumentNotFoundError",
    "EmbeddingError",
    "EmptyDocumentError",
    "IngestionResult",
    "InvalidQueryError",
    "MintRAGError",
    "UnsupportedDocumentTypeError",
    "main",
]


def main() -> None:
    from mintrag.main import main as run

    run()
