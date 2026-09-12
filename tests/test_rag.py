import unittest

from rag.chunking import PolicyChunker
from rag.loaders import TextLoader
from rag.pipeline import RAGPipeline


class TestRAG(unittest.TestCase):

    def test_loader(self):
        loader = TextLoader()
        documents = loader.load_directory("data/sample")

        self.assertEqual(len(documents), 1)
        self.assertGreater(len(documents[0].text), 0)

    def test_chunking(self):
        loader = TextLoader()
        document = loader.load_file("data/sample/policies.txt")

        chunker = PolicyChunker()
        chunks = chunker.chunk(document)

        self.assertEqual(len(chunks), 7)

    def test_retrieval(self):
        rag = RAGPipeline()
        rag.index_directory("data/sample")

        results = rag.retrieve(
            "Can I replace a damaged product?",
            top_k=3,
        )

        self.assertGreater(len(results), 0)
        self.assertEqual(
            results[0].chunk_id,
            "data\\sample\\policies.txt:1",
        )


if __name__ == "__main__":
    unittest.main()