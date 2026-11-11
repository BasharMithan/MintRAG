from mintrag.ingestions.ingestion import Ingestion
from mintrag.models import Chunk, Document


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
