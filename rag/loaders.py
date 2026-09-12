from dataclasses import dataclass
from pathlib import Path


@dataclass
class Document:
    text: str
    source: str


class TextLoader:
    """Load plain-text documents from a file or directory."""

    def load_file(self, path: str | Path) -> Document:
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"Document not found: {path}")

        if not path.is_file():
            raise ValueError(f"Expected a file: {path}")

        return Document(
            text=path.read_text(encoding="utf-8"),
            source=str(path),
        )

    def load_directory(self, directory: str | Path) -> list[Document]:
        directory = Path(directory)

        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")

        if not directory.is_dir():
            raise ValueError(f"Expected a directory: {directory}")

        documents = []

        for path in sorted(directory.glob("*.txt")):
            documents.append(self.load_file(path))

        return documents