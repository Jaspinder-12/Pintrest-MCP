"""
Module: server.py

Purpose:
FastMCP server initialization and tool registry entry point.

Dependencies:
- mcp
- pydantic

Usage:
Run: python src/server.py

Notes:
Registers and exposes visual search tools to MCP-compatible agents.

Future Improvements:
- Support for Server-Sent Events (SSE) server transport modes
- Custom schemas validator integrations
"""

import sys
import os

# Adjust path to import from src relative to the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mcp.server.fastmcp import FastMCP
import json
import logging

from src.pinterest import search_pinterest, get_pin_details, get_board_pins
from src.tools import search_ui_inspiration, search_branding_inspiration, search_design_systems

# ============================================
# PURPOSE
# ============================================
# Initializes the FastMCP application and binds tool routes. Handles parameter 
# serializations and registers standard STDIO connection transport.

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP Server
mcp = FastMCP("Pinterest Search")

# ============================================
# BUSINESS LOGIC
# ============================================

@mcp.tool()
def tool_search_pinterest(query: str) -> str:
    """
    Search Pinterest for visual pins matching the query.

    Parameters:
        query: Keywords representing target visual search.

    Returns:
        str: Serialized JSON results listing matching pins.
    """
    logger.info(f"Executing search_pinterest for query: '{query}'")
    pins = search_pinterest(query)
    results = [pin.model_dump() for pin in pins]
    return json.dumps({"results": results}, indent=2)

@mcp.tool()
def tool_get_pin_details(pin_url: str) -> str:
    """
    Retrieves visual attributes and description text for a specific Pin page.

    Parameters:
        pin_url: Direct link to Pinterest Pin.

    Returns:
        str: Serialized JSON of detailed Pin properties.
    """
    logger.info(f"Retrieving details for Pin URL: '{pin_url}'")
    pin = get_pin_details(pin_url)
    if not pin:
        return json.dumps({"error": "Pin page could not be parsed or downloaded."}, indent=2)
    return json.dumps(pin.model_dump(), indent=2)

@mcp.tool()
def tool_get_board_pins(board_url: str) -> str:
    """
    Lists visual pins saved on a specific Pinterest Board URL.

    Parameters:
        board_url: Direct link to target Board.

    Returns:
        str: Serialized JSON listing pins in the board.
    """
    logger.info(f"Retrieving pins for Board URL: '{board_url}'")
    pins = get_board_pins(board_url)
    results = [pin.model_dump() for pin in pins]
    return json.dumps({"results": results}, indent=2)

@mcp.tool()
def tool_search_ui_inspiration(query: str, platform: str = "web") -> str:
    """
    Shortcut search for user interface layouts, pricing cards, and dashboards.

    Parameters:
        query: Specific UI elements keywords (e.g. pricing card, hero section).
        platform: Platform type (web, mobile, tablet).

    Returns:
        str: Serialized JSON UI design references list.
    """
    logger.info(f"Executing UI inspiration search for: '{query}' ({platform})")
    pins = search_ui_inspiration(query, platform)
    results = [pin.model_dump() for pin in pins]
    return json.dumps({"results": results}, indent=2)

@mcp.tool()
def tool_search_branding_inspiration(query: str, asset_type: str = "logo") -> str:
    """
    Shortcut search for brand identity guidelines, logos, and typography palettes.

    Parameters:
        query: Target brand context (e.g. tech agency, organic cafe).
        asset_type: Brand asset parameter (logo, colors, packaging).

    Returns:
        str: Serialized JSON branding references list.
    """
    logger.info(f"Executing branding inspiration search for: '{query}' ({asset_type})")
    pins = search_branding_inspiration(query, asset_type)
    results = [pin.model_dump() for pin in pins]
    return json.dumps({"results": results}, indent=2)

@mcp.tool()
def tool_search_design_systems(query: str) -> str:
    """
    Shortcut search for design system guides, UI kits, and token guidelines.

    Parameters:
        query: UI component design target (e.g. button variants, spacing).

    Returns:
        str: Serialized JSON design system references list.
    """
    logger.info(f"Executing design system search for: '{query}'")
    pins = search_design_systems(query)
    results = [pin.model_dump() for pin in pins]
    return json.dumps({"results": results}, indent=2)

if __name__ == "__main__":
    # Start FastMCP server runner over standard STDIO interface
    mcp.run()

# ============================================
# AGENT INTERACTION
# ============================================
# LLM agents interface with this server process directly inside IDE terminal 
# runners or custom agent workflows.

# ============================================
# SECURITY NOTES
# ============================================
# Always validate input string sizes to prevent large payload processing.

# ============================================
# FUTURE ENHANCEMENTS
# ============================================
# Configure a HTTP/SSE listener option to allow web-based agent access.

# ============================================
# FUTURE IMPROVEMENTS
# ============================================
#
# 1. Dictionary mapping router instead of condition blocks
# 2. Redis-based cache options integrations
# 3. Dynamic schema updating triggers
# 4. Multi-agent authentication tokens validation
#
# ============================================
