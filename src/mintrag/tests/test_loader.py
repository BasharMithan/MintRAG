import hashlib
import json

import pytest

from mintrag.ingestions.loader import TextDocumentLoader


def testTextDocumentLoaderLoadsPythonFile(tmp_path):
    filePath = tmp_path / "sample.py"
    text = "print(\"hello from mintrag\")\n"
    filePath.write_bytes(text.encode("utf-8"))

    document = TextDocumentLoader().load(str(filePath))

    expectedId = hashlib.sha256(
        json.dumps([str(filePath.resolve()), text], ensure_ascii=False).encode("utf-8")
    ).hexdigest()

    assert document.id == expectedId
    assert document.source == str(filePath.resolve())
    assert document.text == text


def testTextDocumentLoaderRejectsUnsupportedDocumentExtension(tmp_path):
    filePath = tmp_path / "notes.csv"
    filePath.write_text("hello", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported document extension"):
        TextDocumentLoader().load(str(filePath))


def testTextDocumentLoaderRejectsNonFileSource(tmp_path):
    missingFile = tmp_path / "missing.py"

    with pytest.raises(FileNotFoundError):
        TextDocumentLoader().load(str(missingFile))

    with pytest.raises(ValueError, match="Source is not a regular file"):
        TextDocumentLoader().load(str(tmp_path))
