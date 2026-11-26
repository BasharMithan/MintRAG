import numpy as np
from typing import Any

from sentence_transformers import SentenceTransformer
from sentence_transformers.util.tensor import _tensor_to_numpy

from mintrag.config.chunking import EmbeddingConfig
from mintrag.application.ports import Embedder
from mintrag.models.ingestion import Document, Chunk


class SentenceTransformerEmbedder(Embedder):

    def __init__(self, config: EmbeddingConfig) -> None:
        self.config = config
        self.dimentions = 2

        self.model = SentenceTransformer(self.config.model)

    def embeddDocument(self, chunks: tuple[Chunk, ...]) -> list[np.ndarray]:
        if len(chunks) == 0:
            raise ValueError("There is no text in the document.")

        texts = [chunk.text for chunk in chunks]

        embeddings = self.model.encode(texts, batch_size=self.config.batchSize,
                                      normalize_embeddings=True,
                                      convert_to_numpy=False)

        results = [_tensor_to_numpy(embedding) for embedding in embeddings]

        return results

    def embeddQuery(self, text: str) -> np.ndarray[tuple[Any, ...], np.dtype[Any]]:
        ...


# oxml-repoerto -> Retrieval
# Gemini -> Generation
