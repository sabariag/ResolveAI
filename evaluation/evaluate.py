import json
from pathlib import Path

from rag.pipeline import RAGPipeline


DATASET_PATH = Path(__file__).parent / "dataset.json"


def load_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def reciprocal_rank(results, expected_chunk_id):
    for rank, result in enumerate(results, start=1):
        if result.chunk_id == expected_chunk_id:
            return 1 / rank

    return 0.0


def evaluate(top_k: int = 3):
    dataset = load_dataset()

    rag = RAGPipeline()
    rag.index_directory("data/sample")

    hits = 0
    reciprocal_ranks = []

    for item in dataset:
        results = rag.retrieve(
            item["query"],
            top_k=top_k,
        )

        expected_chunk_id = item["expected_chunk_id"]

        hit = any(
            result.chunk_id == expected_chunk_id
            for result in results
        )

        if hit:
            hits += 1

        reciprocal_ranks.append(
            reciprocal_rank(results, expected_chunk_id)
        )

        rank = next(
            (
                index
                for index, result in enumerate(results, start=1)
                if result.chunk_id == expected_chunk_id
            ),
            None,
        )

        print(f"\nQuery: {item['query']}")
        print(f"Expected: {expected_chunk_id}")
        print(f"Rank: {rank if rank else 'Not found'}")

    hit_rate = hits / len(dataset)
    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)

    print("\n--- Evaluation Results ---")
    print(f"Queries: {len(dataset)}")
    print(f"Hit@{top_k}: {hit_rate:.3f}")
    print(f"MRR: {mrr:.3f}")


if __name__ == "__main__":
    evaluate(top_k=3)