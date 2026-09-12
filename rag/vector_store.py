import numpy as np

from rag.chunking import Chunk


class VectorStore:
    """Store chunk embeddings and perform similarity search."""

    def __init__(self):
        self.chunks: list[Chunk] = []
        self.embeddings = None

    def add(self, chunks: list[Chunk], embeddings):
        self.chunks = chunks
        self.embeddings = np.asarray(embeddings)

    def search(self, query_embedding, top_k: int = 3):
        if self.embeddings is None or not self.chunks:
            return []

        query_embedding = np.asarray(query_embedding)

        scores = self.embeddings @ query_embedding
        top_indices = np.argsort(scores)[::-1][:top_k]

        return [
            {
                "chunk": self.chunks[index],
                "score": float(scores[index]),
            }
            for index in top_indices
        ]