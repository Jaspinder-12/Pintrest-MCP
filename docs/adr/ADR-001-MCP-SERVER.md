# ADR-001: Model Context Protocol (MCP) as Core Interface

---
**Document Info:**
* **Date**: 2026-06-09
* **Status**: Approved
* **Author**: Lead Software Architect
* **Notes**: Establishes the primary interface for client integrations.
---

## 1. Context

AI agents (such as Cursor, Cline, and Claude Code) require a standardized protocol to interface with tools, databases, and remote APIs. Traditionally, integration has been built ad-hoc using REST or custom JSON-RPC tunnels, which leads to high integration costs, fragile schemas, and lack of client-side validation.

## 2. Decision

We choose the **Model Context Protocol (MCP)**, open-sourced by Anthropic, as the primary communication protocol. 
* The server will support **STDIO transport** (for local workflows where IDE agents spin up the server as a child process).
* The server will also support **SSE (Server-Sent Events) transport** (for cloud deployments hosting the MCP server for web-based or multi-agent environments).

## 3. Consequences

### Positive
* **Broad Support**: Instantly integrates with Cursor, Cline, Claude Code, and any other MCP-compliant system.
* **Type Safety**: Automatic schema validation of tool inputs and outputs.
* **Context Preservation**: Seamless injection of visual metadata directly into agent prompts.

### Negative
* **Transport Limitations**: STDIO transport limits the server to a single local execution environment per process.
* **Overhead**: Requires mapping standard REST/gRPC endpoints into MCP schemas.

---

# ============================================
# FUTURE IMPROVEMENTS
# ============================================
#
# 1. Automatic schema generator for dynamic custom tool configurations
# 2. End-to-end encryption over SSE channels
#
# ============================================
