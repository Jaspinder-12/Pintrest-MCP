"""
Module: models.py

Purpose:
Pydantic data validation models representing Pinterest entities.

Dependencies:
pydantic

Usage:
Imported by tools and scraper modules to type-check results structures.

Notes:
Ensures clean structure contracts for tool output payloads.

Future Improvements:
- Added layout categories metadata tags
- JSON validation helper methods
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# ============================================
# PURPOSE
# ============================================
# Standardizes the format of Pins and Boards returned by the scraping engine, 
# ensuring clean, type-safe data outputs for MCP agents.

# ============================================
# BUSINESS LOGIC
# ============================================
class PinterestPin(BaseModel):
    """
    Data model representing a single Pinterest Pin asset.
    """
    title: str = Field(..., description="Title of the visual asset or pin")
    pin_url: str = Field(..., description="Direct URL to the Pinterest Pin page")
    image_url: str = Field(..., description="Source direct link to the pin image file")
    board: Optional[str] = Field(None, description="Name of the board containing the pin")
    description: Optional[str] = Field(None, description="Description text accompanying the pin")
    source: Optional[str] = Field(None, description="Original source website link")

class PinterestBoard(BaseModel):
    """
    Data model representing a Pinterest board containing multiple Pins.
    """
    name: str = Field(..., description="Name of the inspiration board")
    board_url: str = Field(..., description="Pinterest URL to the board page")
    description: Optional[str] = Field(None, description="Creative description brief of the board")
    pins: List[PinterestPin] = Field(default_list=[], description="List of pins associated with the board")

# ============================================
# AGENT INTERACTION
# ============================================
# AI agents parse these models to construct Markdown layouts containing image links in their chat interface.

# ============================================
# SECURITY NOTES
# ============================================
# Pydantic validates input types automatically to prevent type injection bugs.

# ============================================
# FUTURE ENHANCEMENTS
# ============================================
# Add validator methods to verify that image_url and pin_url are valid HTTP/HTTPS schemes.

# ============================================
# FUTURE IMPROVEMENTS
# ============================================
#
# 1. URL pattern validation checks
# 2. Base64 thumbnail generation fields mapping
# 3. Dynamic tag classification list attributes
# 4. Color metadata storage schema additions
#
# ============================================
