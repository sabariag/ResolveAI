from dataclasses import dataclass

from rag.vector_store import VectorStore
from rag.embeddings import EmbeddingModel


@dataclass
class RetrievedChunk:
    text: str
    source: str
    chunk_id: str
    score: float


class Retriever:
    """Retrieve the most relevant policy chunks for a query."""

    def __init__(
        self,
        vector_store: VectorStore,
        embedding_model: EmbeddingModel,
    ):
        self.vector_store = vector_store
        self.embedding_model = embedding_model

    def retrieve(self, query: str, top_k: int = 3) -> list[RetrievedChunk]:
        query_embedding = self.embedding_model.encode_query(query)

        results = self.vector_store.search(
            query_embedding,
            top_k=top_k,
        )

        return [
            RetrievedChunk(
                text=result["chunk"].text,
                source=result["chunk"].source,
                chunk_id=result["chunk"].chunk_id,
                score=result["score"],
            )
            for result in results
        ]