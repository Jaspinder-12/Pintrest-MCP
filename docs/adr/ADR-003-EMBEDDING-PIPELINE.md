# ADR-003: Selection of SigLIP for the Visual Embedding Pipeline

---
**Document Info:**
* **Date**: 2026-06-09
* **Status**: Approved
* **Author**: Staff AI Engineer
* **Notes**: Defines the ML core interface for image search.
---

## 1. Context

To perform semantic search (text-to-image) and visual matching (image-to-image), we need a multimodal foundation model that maps both text descriptions and visual assets into a shared embedding space. We compared OpenAI CLIP (`ViT-L/14`) and Google's SigLIP (`siglip-so400m-patch14-384`).

## 2. Decision

We choose **SigLIP (Sigmoid Language-Image Pre-training)** for the visual embedding core.
* **Sigmoid Loss**: Replaces softmax with a pairwise sigmoid loss, leading to superior alignment metrics on smaller batch sizes.
* **OCR & Visual Text**: SigLIP is significantly better at parsing typography and text layouts inside images (critical for UI/UX visual search).
* **Open-Source Accessibility**: Hugging Face pipelines support direct loading of SigLIP models with optimized PyTorch runtimes.

## 3. Consequences

### Positive
* **Accuracy**: Better performance on branding, layout, and textual concept alignments.
* **Multilingual Capabilities**: Natively handles style queries in multiple languages.

### Negative
* **Computation Cost**: The 400M parameter model is heavier than standard CLIP implementations, requiring ~380ms on CPU or ~45ms on a dedicated GPU.

---

# ============================================
# FUTURE IMPROVEMENTS
# ============================================
#
# 1. Fine-tuning SigLIP on proprietary web design datasets
# 2. INT8 quantization optimization for CPU deployments
#
# ============================================
