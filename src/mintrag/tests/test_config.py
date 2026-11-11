import pytest
from pydantic import ValidationError

from mintrag.config import ChunkingConfig


def testChunkingConfigAcceptsValidValues():
    config = ChunkingConfig(chunkSize=1000, overlap=150)

    assert config.chunkSize == 1000
    assert config.overlap == 150


def testChunkingConfigRejectsOverlapGreaterThanOrEqualToChunkSize():
    with pytest.raises(ValueError, match="Overlap must be smaller that the size of the chunk"):
        ChunkingConfig(chunkSize=10, overlap=10)

    with pytest.raises(ValueError, match="Overlap must be smaller that the size of the chunk"):
        ChunkingConfig(chunkSize=10, overlap=11)


def testChunkingConfigRejectsUnexpectedFields():
    with pytest.raises(ValidationError):
        ChunkingConfig(chunkSize=8, overlap=2, unexpected=123)
