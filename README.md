# Minimal Pinterest MCP Server

---
**Module Info:**
* **Module**: README.md
* **Purpose**: Installation guide, local running, and usage workflows.
* **Dependencies**: Python 3.12+, httpx, BeautifulSoup, FastMCP
* **Author**: Core Dev Team
* **Notes**: Simple bridge for AI agents to query Pinterest designs.
---

## 1. Overview
A lightweight, single-service Model Context Protocol (MCP) server that acts as a visual inspiration discovery bridge between AI agents and Pinterest. It scrapes search results, board listings, and pin details directly on the fly.

## 2. Technical Stack
* **Runtime**: Python 3.12+
* **Framework**: FastMCP (MCP Python SDK)
* **Libraries**: `httpx` for requests, `beautifulsoup4` for HTML parsing, `pydantic` for data models.

## 3. Installation & Local Setup

### 3.1 Prerequisite Installation
Ensure you have Python 3.12 installed, then install requirements:
```bash
pip install -r requirements.txt
```

### 3.2 Running the MCP Server
Launch the server over STDIO transport:
```bash
python src/server.py
```

## 4. MCP Manifest Configuration
To connect this server directly to Cursor, Cline, or Claude Code, add the following configuration to your `mcp_config.json`:

```json
{
  "mcpServers": {
    "pinterest": {
      "command": "python",
      "args": ["C:/Users/Jass2/.gemini/antigravity-ide/scratch/pinterest-mcp/src/server.py"]
    }
  }
}
```

---

# ============================================
# FUTURE IMPROVEMENTS
# ============================================
#
# 1. Integrate dynamic HTTP proxy rotation to bypass scrapers blocking
# 2. Add local SQLite caching layer for search queries
#
# ============================================
