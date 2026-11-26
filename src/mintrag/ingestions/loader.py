import hashlib
import json
from pathlib import Path

from pypdf import PdfReader

from mintrag.models import Document


class TextDocumentLoader:
    def load(self, source: str) -> Document:

        supportedExtensions: list[str] = [".txt", ".pdf", ".md", ".py"]

        path = Path(source).expanduser().resolve(strict=True)

        if not path.is_file():
            raise ValueError(f"Source is not a regular file: {path}")

        if path.suffix.lower() not in supportedExtensions:
            raise ValueError(f"Unsupported document extension: {path.suffix}")

        if path.suffix.lower() == ".pdf":
            text = "\n".join(
                page.extract_text() or "" for page in PdfReader(str(path)).pages
            )
        else:
            with path.open("r", encoding="utf-8", newline="") as file:
                text = file.read()

        identity = json.dumps(
            [str(path), text],
            ensure_ascii=False,
        ).encode("utf-8")

        return Document(
            id=hashlib.sha256(identity).hexdigest(), source=str(path), text=text
        )


if __name__ == "__main__":
    from pprint import pprint

    path = "src/mintrag/samples/sample.txt"

    loader = TextDocumentLoader()
    document = loader.load(source=path)

    pprint(document)
