# ADR-002: Selection of Qdrant as the Vector Database

---
**Document Info:**
* **Date**: 2026-06-09
* **Status**: Approved
* **Author**: Lead Data Architect
* **Notes**: Governs visual embedding search optimization.
---

## 1. Context

Storing and querying high-dimensional vector embeddings (768-d from SigLIP) requires a highly performant vector database. The database must support:
1. Low-latency Cosine similarity searches (< 50ms).
2. Advanced payload filtering (e.g. filtering vectors based on SQL relational tags like `user_id`, `colors`, `category`).
3. Simple horizontal scaling.
4. Active open-source development and healthy community support.

We evaluated three options: pgvector (PostgreSQL extension), Milvus (distributed architecture), and Qdrant (Rust-based).

## 2. Decision

We choose **Qdrant** as the primary vector database.
* **Rust Core**: Ensures high memory efficiency and speed.
* **Payload Filtering**: Highly optimized filter evaluation during HNSW index construction.
* **Qdrant Cloud**: Provides an easy path from self-hosted local setups to enterprise scaling.

## 3. Consequences

### Positive
* **Performance**: Consistently outperforms pgvector on high-recall indexing benchmarks.
* **Developer Experience**: Clear JSON REST and gRPC API wrappers.
* **Memory Management**: Low memory overhead compared to Java/Go alternatives.

### Negative
* **Multi-Database Management**: Requires synchronization between PostgreSQL (relational metadata) and Qdrant (vectors), introducing potential eventual consistency issues.

---

# ============================================
# FUTURE IMPROVEMENTS
# ============================================
#
# 1. Automating transactional vector-relational rollbacks
# 2. Dynamic Qdrant partition indexing for enterprise workspaces
#
# ============================================
