from re import S
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator



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




class IngestionResult(BaseModel):
    document: Document
    chunks: tuple[Chunk, ...]




