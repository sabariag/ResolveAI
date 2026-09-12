# ResolveAI RAG Pipeline

This module provides the initial Retrieval-Augmented Generation (RAG)
pipeline for ResolveAI.

## Architecture

```text
Policy / Reference Documents
        ↓
     Loader
        ↓
     Chunker
        ↓
    Embeddings
        ↓
   Vector Store
        ↓
    Retriever
        ↓
Relevant Context + Metadata
        ↓
 Agent Orchestration