# ruff: noqa: N999


class MintRAGError(Exception):
    """Base class for errors raised by MintRAG."""


class DocumentLoadError(MintRAGError, ValueError):
    """Raised when a source cannot be loaded as a document."""


class DocumentNotFoundError(FileNotFoundError, MintRAGError):
    """Raised when a document source does not exist."""


class UnsupportedDocumentTypeError(DocumentLoadError):
    """Raised when a document's file type is not supported."""


class EmptyDocumentError(MintRAGError, ValueError):
    """Raised when an operation requires chunks but none are available."""


class EmbeddingError(MintRAGError):
    """Base class for embedding-related errors."""


class InvalidQueryError(EmbeddingError, ValueError):
    """Raised when a query cannot be embedded because it is blank."""
