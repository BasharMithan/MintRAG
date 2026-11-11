from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ChunkingConfig(BaseModel):
    "Validated configuration for character-based chunking."

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        strict=True
    )

    chunkSize: int = Field(default=1000, gt=0)
    overlap: int = Field(default=150, ge=0)

    @model_validator(mode="after")
    def validateOverlap(self) -> Self:
        if self.overlap >= self.chunkSize:
            raise ValueError("Overlap must be smaller that the size of the chunk.")

        return self
