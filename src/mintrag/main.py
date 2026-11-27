from langchain_core.documents import Document as LangChainDocument
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

from mintrag.config import ChunkingConfig
from mintrag.customExceptions import EmptyDocumentError
from mintrag.ingestions.chunker import CharacterChunker
from mintrag.ingestions.loader import TextDocumentLoader


def main(source: str = "src/mintrag/samples/sample.md") -> None:
    document = TextDocumentLoader().load(source)
    chunks = CharacterChunker(ChunkingConfig(chunkSize=1000, overlap=150)).split(
        document
    )
    document.chunks = chunks

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs={"normalize_embeddings": True},
    )
    vector_store = InMemoryVectorStore(embedding=embeddings)

    documents = [
        LangChainDocument(
            id=chunk.id,
            page_content=chunk.text,
            metadata={
                "documentID": chunk.documentID,
                "source": chunk.source,
                "index": chunk.index,
                "start": chunk.start,
                "end": chunk.end,
            },
        )
        for chunk in chunks
    ]

    if not documents:
        raise EmptyDocumentError("The document contains no text chunks.")

    vector_store.add_documents(
        documents=documents,
        ids=[chunk.id for chunk in chunks],
    )

    results = vector_store.similarity_search(
        query="What are the default chunk size and overlap?",
        k=3,
    )

    for document in results:
        print(f"Source: {document.metadata['source']}")
        print(document.page_content)


if __name__ == "__main__":
    main()
