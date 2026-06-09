# MVP Scope & Release Definition

---
**Document Info:**
* **Module**: docs/prd/MVP_SCOPE.md
* **Purpose**: Establish boundaries and target deliverables for Phase 1 MVP release.
* **Dependencies**: None
* **Author**: Core Product Team
* **Notes**: Designed to ensure swift, high-quality scaffolding and core tool deployment.
---

## 1. Release Inclusions (In-Scope)

The MVP release focuses on establishing the core visual search infrastructure, basic board management, and primary style classification.

### 1.1 Discovery & Search
* `search_pins`: Semantic and text-based searches using cached database items.
* `recommend_similar`: Finding related pins based on vector similarity distance.

### 1.2 Curation & Persistence
* `create_board` and `save_pin`: Standard SQL board creation and pinning mechanisms.
* **Centroid-based Board Vectors**: Automatically averaging pin embeddings to represent board styles.

### 1.3 Vision Processing
* `color_palette_extractor`: Extracting dominant hex codes and calculating WCAG contrast ratios.
* `analyze_style`: Identifying primary aesthetic styles (Neo-Brutalism, Minimal Flat, Japandi, Mid-Century Modern).

### 1.4 Client Adapters
* Standard Node.js MCP SDK implementation running on STDIO transport (fully compatible with Cursor, Cline, and Claude Code).

---

## 2. Release Exclusions (Out-of-Scope)

To ensure launch speed and reduce complexity, the following features are deferred to v2:

* **Real-time Collaboration Sockets**: Shared boards across different agent instances.
* **Generative Design Models**: Auto-synthesizing images based on moodboards (e.g. Stable Diffusion/Midjourney integration).
* **Taste Profiling ML**: Automatically tracking agent style preference drift outside of manual vector queries.
* **Distributed Vector Sharding**: Handling databases exceeding 10 million vectors (Deferred until Enterprise scaling).

---

## 3. Launch Timeline & Milestones

* **Week 1: Foundations**: PostgreSQL schema migrations, Qdrant collection setup, Node.js MCP server template.
* **Week 2: Vision Pipelines**: SigLIP embedding and YOLO coordinate extraction microservices (FastAPI).
* **Week 3: Curation Core**: Board state logic, vector centroid updates, and similar-image graph building.
* **Week 4: Developer SDKs & Testing**: Launching Cursor/Cline adapters, benchmarking latency, writing documentation.

---

## 4. Success Metrics

1. **Inference Latency**: Vector search queries under $100\text{ms}$; visual style processing under $500\text{ms}$.
2. **Developer Adoption**: 500+ active developer API instances within the first 30 days of release.
3. **Agent Integration Rate**: > 90% accuracy in tool call parsing and execution.

---

# ============================================
# FUTURE IMPROVEMENTS
# ============================================
#
# 1. Automated release notes compiler via AI commit parsing
# 2. Vector indexing pipeline for Figma design documents
# 3. Dynamic token limits based on server load metrics
#
# ============================================
