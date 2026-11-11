from mintrag.config import ChunkingConfig
from mintrag.ingestions.chunker import CharacterChunker
from mintrag.models import Document


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
