# RAG Evaluation

This directory contains the evaluation dataset and evaluation script
for the ResolveAI RAG retrieval pipeline.

## Dataset

`dataset.json` contains representative customer-resolution queries
and the policy chunk expected to be retrieved.

The current dataset covers:

- Damaged product replacement
- Refunds
- Order cancellation
- Replacement inventory
- Customer verification
- Escalation

## Metrics

The evaluation reports:

### Hit@K

Measures whether the expected chunk appears within the top K retrieved
results.

### Mean Reciprocal Rank (MRR)

Measures how highly the expected chunk is ranked.

A score of `1.0` means the expected result was ranked first for every
query.

## Baseline Result

Using the current sample dataset:

- Queries: 6
- Hit@3: 1.000
- MRR: 1.000
- Expected chunk rank: 1 for all six queries

This is a small prototype evaluation dataset and should not be treated
as a general measure of production retrieval quality.

## Running Evaluation

From the repository root:

```powershell
python -m evaluation.evaluate