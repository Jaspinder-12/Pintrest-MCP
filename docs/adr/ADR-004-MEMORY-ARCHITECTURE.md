# ADR-004: Board Vector Centroid for Agent Memory Management

---
**Document Info:**
* **Date**: 2026-06-09
* **Status**: Approved
* **Author**: Lead Architect
* **Notes**: Governs long-term visual memory retrieval.
---

## 1. Context

AI agents need a way to build a cohesive visual style profile over a session without overloading the context window with individual image metadata. When an agent retrieves inspiration from a board containing 50 pins, parsing the JSON metadata of all 50 pins consumes excessive token bandwidth.

## 2. Decision

We implement the **Vector Centroid** calculation for boards:
1. Every time a Pin is saved to a Board, an async worker calculates the mathematical centroid of all Pin vector embeddings:

$$\vec{C}_{board} = \frac{1}{N} \sum_{i=1}^{N} \vec{V}_{pin\_i}$$

2. We store this centroid vector directly in the `boards` database table and index it in the Qdrant `board_embeddings` collection.
3. When the agent requests the board's aesthetic context, the server sends the centroid vector or uses it to query the nearest style neighbors, providing a compressed representation of the board's visual identity.

## 3. Consequences

### Positive
* **Extreme Compression**: Compresses an entire board's style profile into a single 768-dimensional vector.
* **Style Drift Analysis**: Allows agents to track how the project's art direction changes over time by analyzing historical centroid values.

### Negative
* **Loss of Detail**: Averaging vectors can lose fine-grained details if the board contains highly disparate images. The system mitigates this by alerting agents if a board's clustering variance exceeds a predefined threshold.

---

# ============================================
# FUTURE IMPROVEMENTS
# ============================================
#
# 1. Multi-modal centroid clustering for complex design systems
# 2. Real-time notification triggers for high style-variance boards
#
# ============================================
