from dataclasses import dataclass

from rag.loaders import Document


@dataclass
class Chunk:
    text: str
    source: str
    chunk_id: str


class PolicyChunker:
    """Split policy documents into retrievable chunks."""

    def chunk(self, document: Document) -> list[Chunk]:
        sections = [
            section.strip()
            for section in document.text.split("\n\n")
            if section.strip()
        ]

        chunks = []

        for index, section in enumerate(sections):
            chunks.append(
                Chunk(
                    text=section,
                    source=document.source,
                    chunk_id=f"{document.source}:{index}",
                )
            )

        return chunks