
import hashlib
import json

from mintrag.config import ChunkingConfig
from mintrag.models import Chunk, Document


class CharacterChunker:
    def __init__(self, config: ChunkingConfig) -> None:
        self.config = config


    def split(self, document: Document) -> tuple[Chunk, ...]:
        chunks: list[Chunk] = []

        length = len(document.text)
        step = self.config.chunkSize - self.config.overlap

        for start in range(0, length, step):
            end = min(start + self.config.chunkSize, length)
            text = document.text[start:end]

            if text.strip():
                chunks.append(
                    Chunk(
                        id=self.generateChunkID(documentID=document.id,start=start,end=end),
                        documentID=document.id,
                        source=document.source,
                        text=text,
                        index=len(chunks),
                        start=start,
                        end=end
                        ))

            if end == length:
                break

        return tuple(chunks)


    def generateChunkID(self, *, documentID: str, start: int, end: int) -> str:
        identity = json.dumps(
            [
                "character-v1",
                documentID,
                self.config.chunkSize,
                self.config.overlap,
                start,
                end,
            ],
            separators=(",", ":"),
        )

        return hashlib.sha256(identity.encode("utf-8")).hexdigest()