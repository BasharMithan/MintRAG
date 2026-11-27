import numpy as np
import pytest

from mintrag.config import EmbeddingConfig
from mintrag.customExceptions import (
    DocumentNotFoundError,
    EmptyDocumentError,
    InvalidQueryError,
    MintRAGError,
    UnsupportedDocumentTypeError,
)
from mintrag.embeddings import embedding
from mintrag.ingestions.loader import TextDocumentLoader
from mintrag.main import main
from mintrag.models import Chunk, Document


def testCustomDocumentErrorsInheritFromMintRAGError(tmp_path):
    missingFile = tmp_path / "missing.txt"
    unsupportedFile = tmp_path / "notes.csv"
    unsupportedFile.write_text("not supported", encoding="utf-8")

    with pytest.raises(DocumentNotFoundError) as missingError:
        TextDocumentLoader().load(str(missingFile))
    with pytest.raises(UnsupportedDocumentTypeError) as unsupportedError:
        TextDocumentLoader().load(str(unsupportedFile))

    assert isinstance(missingError.value, MintRAGError)
    assert isinstance(missingError.value, FileNotFoundError)
    assert isinstance(unsupportedError.value, MintRAGError)
    assert isinstance(unsupportedError.value, ValueError)


def testTextDocumentLoaderExtractsPdfText(monkeypatch, tmp_path):
    class FakePage:
        def __init__(self, text):
            self.text = text

        def extract_text(self):
            return self.text

    class FakePdfReader:
        def __init__(self, source):
            assert source.endswith("sample.pdf")
            self.pages = [FakePage("first page"), FakePage(None), FakePage("last page")]

    pdfPath = tmp_path / "sample.pdf"
    pdfPath.write_bytes(b"test pdf")
    monkeypatch.setattr("mintrag.ingestions.loader.PdfReader", FakePdfReader)

    document = TextDocumentLoader().load(str(pdfPath))

    assert document.text == "first page\n\nlast page"
    assert document.source == str(pdfPath.resolve())


def testEmbeddingConfigValidatesModelAndBatchSize():
    assert EmbeddingConfig(model="  encoder  ", batchSize=4).model == "encoder"

    with pytest.raises(ValueError, match="Model name must not be blank"):
        EmbeddingConfig(model="   ")
    with pytest.raises(ValueError):
        EmbeddingConfig(batchSize=0)


def testSentenceTransformerEmbedderEmbedsDocumentsAndQueries(monkeypatch):
    class FakeSentenceTransformer:
        def __init__(self, modelName):
            assert modelName == "test-model"

        def get_sentence_embedding_dimension(self):
            return 2

        def encode(self, texts, **kwargs):
            assert kwargs["normalize_embeddings"] is True
            if isinstance(texts, str):
                return np.array([0.6, 0.8])
            assert kwargs["batch_size"] == 4
            return np.array([[0.1, 0.2], [0.3, 0.4]])

    monkeypatch.setattr(embedding, "SentenceTransformer", FakeSentenceTransformer)
    embedder = embedding.SentenceTransformerEmbedder(
        EmbeddingConfig(model="test-model", batchSize=4)
    )
    document = Document(
        id="doc-1",
        source="sample.txt",
        text="one two",
        chunks=(
            Chunk(
                id="chunk-1",
                documentID="doc-1",
                source="sample.txt",
                text="one",
                index=0,
                start=0,
                end=3,
            ),
            Chunk(
                id="chunk-2",
                documentID="doc-1",
                source="sample.txt",
                text="two",
                index=1,
                start=4,
                end=7,
            ),
        ),
    )

    embeddedDocument = embedder.embeddDocument(document)
    queryEmbedding = embedder.embeddQuery("question")

    assert embeddedDocument.embeddings == ((0.1, 0.2), (0.3, 0.4))
    assert embedder.dimentions == 2
    np.testing.assert_array_equal(
        queryEmbedding, np.array([0.6, 0.8], dtype=np.float32)
    )


def testSentenceTransformerEmbedderRaisesCustomErrorsForInvalidInput(monkeypatch):
    class FakeSentenceTransformer:
        def __init__(self, modelName):
            pass

        def get_sentence_embedding_dimension(self):
            return 2

    monkeypatch.setattr(embedding, "SentenceTransformer", FakeSentenceTransformer)
    embedder = embedding.SentenceTransformerEmbedder(EmbeddingConfig())
    document = Document(id="doc-1", source="empty.txt", text="", chunks=())

    with pytest.raises(EmptyDocumentError) as emptyError:
        embedder.embeddDocument(document)
    with pytest.raises(InvalidQueryError) as queryError:
        embedder.embeddQuery("  ")

    assert isinstance(emptyError.value, ValueError)
    assert isinstance(queryError.value, ValueError)


def testMainStoresChunksAndPrintsRetrievedResults(monkeypatch, capsys):
    class FakeLoader:
        def load(self, source):
            assert source == "input.txt"
            return Document(
                id="doc-1",
                source=source,
                text="MintRAG stores searchable text chunks.",
            )

    class FakeEmbeddings:
        def __init__(self, **kwargs):
            assert kwargs["model_name"] == "sentence-transformers/all-MiniLM-L6-v2"

    class FakeVectorStore:
        def __init__(self, embedding):
            self.embedding = embedding

        def add_documents(self, documents, ids):
            self.documents = documents
            self.ids = ids

        def similarity_search(self, query, k):
            assert query == "What are the default chunk size and overlap?"
            assert k == 3
            return self.documents[:1]

    monkeypatch.setattr("mintrag.main.TextDocumentLoader", FakeLoader)
    monkeypatch.setattr("mintrag.main.HuggingFaceEmbeddings", FakeEmbeddings)
    monkeypatch.setattr("mintrag.main.InMemoryVectorStore", FakeVectorStore)

    main("input.txt")

    output = capsys.readouterr().out
    assert "Source: input.txt" in output
    assert "MintRAG stores searchable text chunks." in output


def testMainRaisesEmptyDocumentErrorWhenNoTextChunks(monkeypatch):
    class FakeLoader:
        def load(self, source):
            return Document(id="doc-1", source=source, text="   ")

    class FakeEmbeddings:
        def __init__(self, **kwargs):
            pass

    class FakeVectorStore:
        def __init__(self, embedding):
            pass

    monkeypatch.setattr("mintrag.main.TextDocumentLoader", FakeLoader)
    monkeypatch.setattr("mintrag.main.HuggingFaceEmbeddings", FakeEmbeddings)
    monkeypatch.setattr("mintrag.main.InMemoryVectorStore", FakeVectorStore)

    with pytest.raises(EmptyDocumentError):
        main("empty.txt")
