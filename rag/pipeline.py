from rag.chunking import PolicyChunker
from rag.embeddings import EmbeddingModel
from rag.loaders import TextLoader
from rag.retriever import RetrievedChunk, Retriever
from rag.vector_store import VectorStore


class RAGPipeline:
    """End-to-end pipeline for loading, indexing, and retrieving documents."""

    def __init__(
        self,
        embedding_model_name: str = "all-MiniLM-L6-v2",
    ):
        self.loader = TextLoader()
        self.chunker = PolicyChunker()
        self.embedding_model = EmbeddingModel(embedding_model_name)
        self.vector_store = VectorStore()
        self.retriever = Retriever(
            vector_store=self.vector_store,
            embedding_model=self.embedding_model,
        )

    def index_directory(self, directory: str):
        """Load and index all supported documents in a directory."""

        documents = self.loader.load_directory(directory)

        all_chunks = []

        for document in documents:
            all_chunks.extend(self.chunker.chunk(document))

        if not all_chunks:
            raise ValueError(f"No documents found in: {directory}")

        embeddings = self.embedding_model.encode_documents(
            [chunk.text for chunk in all_chunks]
        )

        self.vector_store.add(
            chunks=all_chunks,
            embeddings=embeddings,
        )

        return {
            "documents": len(documents),
            "chunks": len(all_chunks),
        }

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[RetrievedChunk]:
        """Retrieve relevant chunks for a user query."""

        return self.retriever.retrieve(
            query=query,
            top_k=top_k,
        )