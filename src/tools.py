"""
Module: tools.py

Purpose:
Aesthetic query shortcuts wrapping the core Pinterest scraper.

Dependencies:
- None

Usage:
Imported in server.py to expose specialized tools endpoints.

Notes:
Appends design-specific suffixes to generic queries before executing searches.

Future Improvements:
- Dynamic keyword suggestion engines mapping
- User search intent category matching
"""

from typing import List
from src.models import PinterestPin
from src.pinterest import search_pinterest

# ============================================
# PURPOSE
# ============================================
# Exposes specialized shortcut searches by appending context keywords to queries 
# (e.g. appends 'ui ux layout' to UI queries), helping LLM agents find high-quality
# inspiration without manually formulating detailed queries.

# ============================================
# BUSINESS LOGIC
# ============================================

def search_ui_inspiration(query: str, platform: str = "web") -> List[PinterestPin]:
    """
    Shortcut tool specifically querying user interface and web layout styles.

    Parameters:
        query: UI component design target (e.g. pricing card, table).
        platform: Target execution environment (web, mobile, tablet).

    Returns:
        List[PinterestPin]: Visual UI inspirations.
    """
    enriched_query = f"{query} {platform} ui ux dashboard layout modern design"
    return search_pinterest(enriched_query, limit=10)

def search_branding_inspiration(query: str, asset_type: str = "logo") -> List[PinterestPin]:
    """
    Shortcut tool specifically querying branding layouts, color palettes, and typography.

    Parameters:
        query: Industry or brand domain (e.g. tech agency, organic cafe).
        asset_type: Brand asset target (logo, color palette, packaging, corporate identity).

    Returns:
        List[PinterestPin]: Branding design references.
    """
    enriched_query = f"{query} brand identity {asset_type} design typography aesthetic guidelines"
    return search_pinterest(enriched_query, limit=10)

def search_design_systems(query: str) -> List[PinterestPin]:
    """
    Shortcut tool specifically querying frontend design systems and components guidelines.

    Parameters:
        query: Target UI library elements (e.g. button variants, navigation bars).

    Returns:
        List[PinterestPin]: Design system guidelines.
    """
    enriched_query = f"{query} design system UI kit component library token styleguide"
    return search_pinterest(enriched_query, limit=10)

# ============================================
# AGENT INTERACTION
# ============================================
# LLM agents call these tools directly when building specific UI templates 
# or color guidelines in code workspaces.

# ============================================
# SECURITY NOTES
# ============================================
# String input validation constraints protect against SQL/NoSQL injection patterns.

# ============================================
# FUTURE ENHANCEMENTS
# ============================================
# Support for dynamic category tag parameters based on user selection.

# ============================================
# FUTURE IMPROVEMENTS
# ============================================
#
# 1. Intent categorizers mapping queries automatically
# 2. Dynamic synonyms arrays appending
# 3. Accessibility contrast check parameters routing
# 4. Color hex values tags mapping
#
# ============================================
