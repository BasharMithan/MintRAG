# MintRAG

MintRAG is a small Retrieval-Augmented Generation (RAG) prototype for loading
documents, splitting them into searchable chunks, embedding the chunks, and
retrieving relevant text.

## Features

- Loads `.txt`, `.md`, and `.pdf` documents.
- Splits text into overlapping character chunks with stable IDs and source
  offsets.
- Embeds text with Sentence Transformers.
- Runs similarity search with LangChain's in-memory vector store.
- Provides custom exceptions under `mintrag.customExceptions`.

The current command-line demo loads `src/mintrag/samples/sample.md`, uses a
chunk size of 1,000 characters with 150 characters of overlap, and prints the
top three matches for its sample query. The embedding model is downloaded by
the Hugging Face/Sentence Transformers libraries on first use. The vector store
is in memory and is not persisted between runs.

## Requirements

- Python 3.14 or newer
- [uv](https://docs.astral.sh/uv/)

## Install

From the repository root, synchronize the project and development dependencies:

```powershell
uv sync --group dev
```

## Run

```powershell
uv run mintrag
```

To run the module instead:

```powershell
uv run python -m mintrag
```

The demo needs access to the configured Hugging Face model the first time it
runs.

## Use a different source

The Python entry point accepts a source path:

```python
from mintrag.main import main

main("path/to/document.md")
```

The demo query and chunking settings are currently defined in
`src/mintrag/main.py`.

## Tests

Run the test suite with:

```powershell
uv run --group dev pytest
```
