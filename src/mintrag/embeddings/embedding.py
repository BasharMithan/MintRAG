from typing import Any

import numpy as np
from sentence_transformers import SentenceTransformer

from mintrag.application.ports import Embedder
from mintrag.config.chunking import EmbeddingConfig
from mintrag.customExceptions import EmptyDocumentError, InvalidQueryError
from mintrag.models.ingestion import Document


class SentenceTransformerEmbedder(Embedder):
    def __init__(self, config: EmbeddingConfig) -> None:
        self.config = config
        self.model = SentenceTransformer(self.config.model)
        self.dimentions = self.model.get_sentence_embedding_dimension()

    def embeddDocument(self, document: Document) -> Document:
        if not document.chunks or len(document.chunks) == 0:
            raise EmptyDocumentError("There is no text in the document.")

        texts = [chunk.text for chunk in document.chunks]

        embeddings = self.model.encode(
            texts,
            batch_size=self.config.batchSize,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

        # results = [_tensor_to_numpy(embedding) for embedding in embeddings]

        document.embeddings = tuple(
            tuple(float(value) for value in embedding) for embedding in embeddings
        )

        return document

    def embeddQuery(self, text: str) -> np.ndarray[tuple[Any, ...], np.dtype[Any]]:
        if not text.strip():
            raise InvalidQueryError("Query text must not be empty.")

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )
        return np.asarray(embedding, dtype=np.float32).reshape(-1)


# oxml-repoerto -> Retrieval
# Gemini -> Generation
