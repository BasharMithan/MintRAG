import hashlib
import json

import pytest
from pydantic import ValidationError

from mintrag.domain.models import Chunk, Document
from mintrag.ingestions.chunker import CharacterChunker
from mintrag.ingestions.config import ChunkingConfig
from mintrag.ingestions.ingestion import Ingestion
from mintrag.ingestions.loader import TextDocumentLoader


class FakeLoader:
    def __init__(self, document):
        self.document = document

    def load(self, source):
        assert source == "dummy.py"
        return self.document


class FakeChunker:
    def __init__(self, chunks):
        self.chunks = chunks

    def split(self, document):
        assert document.id == "doc-123"
        return self.chunks


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
        ChunkingConfig(chunkSize=8, overlap=2)


def testCharacterChunkerSplitsDocumentIntoOverlappingChunks():
    document = Document(
        id="doc-1",
        source="/tmp/example.py",
        text="abcdefghij",
    )
    chunker = CharacterChunker(ChunkingConfig(chunkSize=4, overlap=1))

    chunks = chunker.split(document)

    assert [chunk.text for chunk in chunks] == ["abcd", "defg", "ghij"]
    assert [chunk.index for chunk in chunks] == [0, 1, 2]
    assert [(chunk.start, chunk.end) for chunk in chunks] == [(0, 4), (3, 7), (6, 10)]
    assert all(chunk.documentID == "doc-1" for chunk in chunks)
    assert all(chunk.source == "/tmp/example.py" for chunk in chunks)


def testCharacterChunkerSkipsWhitespaceOnlyChunks():
    document = Document(
        id="doc-2",
        source="/tmp/whitespace.py",
        text="     ",
    )
    chunker = CharacterChunker(ChunkingConfig(chunkSize=2, overlap=1))

    chunks = chunker.split(document)

    assert chunks == ()


def testCharacterChunkerGenerateChunkIdIsStable():
    chunker = CharacterChunker(ChunkingConfig(chunkSize=4, overlap=1))

    first = chunker.generateChunkID(documentID="doc-3", start=0, end=4)
    second = chunker.generateChunkID(documentID="doc-3", start=0, end=4)
    third = chunker.generateChunkID(documentID="doc-3", start=0, end=5)

    assert first == second
    assert first != third


def testTextDocumentLoaderLoadsPythonFile(tmp_path):
    filePath = tmp_path / "sample.py"
    text = "print(\"hello from mintrag\")\n"
    filePath.write_text(text, encoding="utf-8")

    document = TextDocumentLoader().load(str(filePath))

    expectedId = hashlib.sha256(
        json.dumps([str(filePath.resolve()), text], ensure_ascii=False).encode("utf-8")
    ).hexdigest()

    assert document.id == expectedId
    assert document.source == str(filePath.resolve())
    assert document.text == text


def testTextDocumentLoaderRejectsUnsupportedDocumentExtension(tmp_path):
    filePath = tmp_path / "notes.txt"
    filePath.write_text("hello", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported document extension"):
        TextDocumentLoader().load(str(filePath))


def testTextDocumentLoaderRejectsNonFileSource(tmp_path):
    missingFile = tmp_path / "missing.py"

    with pytest.raises(FileNotFoundError):
        TextDocumentLoader().load(str(missingFile))

    with pytest.raises(ValueError, match="Source is not a regular file"):
        TextDocumentLoader().load(str(tmp_path))


def testIngestionLoadsDocumentAndSplitsIntoChunks():
    document = Document(
        id="doc-123",
        source="dummy.py",
        text="example text",
    )
    chunks = (
        Chunk(
            id="chunk-1",
            documentID="doc-123",
            source="dummy.py",
            text="example",
            index=0,
            start=0,
            end=7,
        ),
        Chunk(
            id="chunk-2",
            documentID="doc-123",
            source="dummy.py",
            text=" text",
            index=1,
            start=7,
            end=12,
        ),
    )

    result = Ingestion(loader=FakeLoader(document), chunker=FakeChunker(chunks)).ingest("dummy.py")

    assert result.document == document
    assert result.chunks == chunks
