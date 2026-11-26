from mintrag.ingestions.chunker import CharacterChunker
from mintrag.config.chunking import ChunkingConfig, EmbeddingConfig
from mintrag.ingestions.loader import TextDocumentLoader
from mintrag.embeddings.embedding import SentenceTransformerEmbedder

def main():
    chunker = CharacterChunker(config=ChunkingConfig())
    loader = TextDocumentLoader()
    path = "src/mintrag/samples/sample.md"
    document = loader.load(path)
    
    chunks = chunker.split(document)
    print(len(chunks))
    embedder = SentenceTransformerEmbedder(config=EmbeddingConfig())
    embeddings = embedder.embeddDocument(chunks=chunks)
    print(embeddings)


if __name__ == "__main__":
    main()