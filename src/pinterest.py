"""
Module: pinterest.py

Purpose:
Pinterest scraping and parsing engine.

Dependencies:
- httpx
- beautifulsoup4
- pydantic

Usage:
Imported by tools.py and server.py to execute web scraping tasks.

Notes:
Utilizes robust JSON extraction fallbacks to parse Client-side state.

Future Improvements:
- Proxy rotation setups to bypass scrape protections
- Selenium/Playwright backup drivers for dynamic page parsing
"""

import httpx
import json
import logging
from bs4 import BeautifulSoup
from typing import List, Optional
import urllib.parse

from src.models import PinterestPin
from src.config import get_settings

# ============================================
# PURPOSE
# ============================================
# Connects to Pinterest via HTTP client, extracts raw HTML structures, and parses 
# initial state JSON blocks or DOM elements to retrieve visual pins.

logger = logging.getLogger(__name__)
settings = get_settings()

def get_http_headers() -> dict:
    """
    Returns common browser headers for requests.

    Returns:
        dict: Headers mapping.
    """
    return {
        "User-Agent": settings.USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/"
    }

def parse_pins_from_json_state(json_data: dict) -> List[PinterestPin]:
    """
    Extracts pin attributes from Pinterest's structured internal JSON state.

    Parameters:
        json_data: Parsed state JSON dictionary.

    Returns:
        List[PinterestPin]: List of extracted Pins.
    """
    pins = []
    
    # Recursively search for pin-like objects in the JSON state
    def search_keys(data: any):
        if isinstance(data, dict):
            # Check for standard Pin keys
            if "images" in data and "id" in data:
                try:
                    pin_id = data["id"]
                    img_url = data.get("images", {}).get("orig", {}).get("url") or \
                              data.get("images", {}).get("736x", {}).get("url")
                    
                    if img_url:
                        title = data.get("title") or data.get("grid_title") or f"Pin {pin_id}"
                        description = data.get("description") or data.get("description_text") or ""
                        source = data.get("link") or data.get("domain") or ""
                        board_name = data.get("board", {}).get("name") or "Inspiration"
                        
                        pins.append(PinterestPin(
                            title=title,
                            pin_url=f"https://www.pinterest.com/pin/{pin_id}/",
                            image_url=img_url,
                            board=board_name,
                            description=description,
                            source=source
                        ))
                except Exception as e:
                    logger.debug(f"Failed to parse pin JSON block: {e}")
            else:
                for v in data.values():
                    search_keys(v)
        elif isinstance(data, list):
            for item in data:
                search_keys(item)

    search_keys(json_data)
    return pins

def search_pinterest(query: str, limit: int = 10) -> List[PinterestPin]:
    """
    Searches Pinterest using raw query strings and extracts matched pins.

    Parameters:
        query: Text search terms.
        limit: Max pin count to return.

    Returns:
        List[PinterestPin]: List of visual pins.

    Notes:
        Falls back to DOM anchor extraction if JSON script tags are missing.
    """
    encoded_query = urllib.parse.quote_plus(query)
    url = f"{settings.PINTEREST_BASE_URL}/search/pins/?q={encoded_query}"
    
    try:
        with httpx.Client(follow_redirects=True, timeout=settings.REQUEST_TIMEOUT_SECONDS) as client:
            response = client.get(url, headers=get_http_headers())
            
        if response.status_code != 200:
            logger.warning(f"Pinterest search returned status code {response.status_code}")
            return []
            
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 1. Primary Strategy: Parse initial JSON state block
        pws_data_script = soup.find("script", id="__PWS_DATA__")
        if pws_data_script and pws_data_script.string:
            try:
                js_state = json.loads(pws_data_script.string)
                pins = parse_pins_from_json_state(js_state)
                if pins:
                    return pins[:limit]
            except Exception as e:
                logger.error(f"Failed to parse PWS data JSON: {e}")
                
        # 2. Secondary Strategy: Parse standard script tag state
        initial_state_script = soup.find("script", id="initial-state")
        if initial_state_script and initial_state_script.string:
            try:
                js_state = json.loads(initial_state_script.string)
                pins = parse_pins_from_json_state(js_state)
                if pins:
                    return pins[:limit]
            except Exception as e:
                logger.error(f"Failed to parse initial state JSON: {e}")

        # 3. Tertiary Fallback: DOM Parsing of anchors and images
        pins = []
        anchors = soup.find_all("a", href=True)
        for anchor in anchors:
            href = anchor["href"]
            if href.startswith("/pin/"):
                img = anchor.find("img")
                if img and img.get("src"):
                    pin_id = href.split("/")[2]
                    pins.append(PinterestPin(
                        title=img.get("alt") or f"Pin {pin_id}",
                        pin_url=f"https://www.pinterest.com{href}",
                        image_url=img["src"],
                        board="Search Results",
                        description="",
                        source=""
                    ))
                    if len(pins) >= limit:
                        break
        return pins

    except Exception as e:
        logger.error(f"Error executing search_pinterest: {e}")
        return []

def get_pin_details(pin_url: str) -> Optional[PinterestPin]:
    """
    Fetches detailed metadata for a specific Pin page.

    Parameters:
        pin_url: Direct link to target Pin.

    Returns:
        Optional[PinterestPin]: Detailed pin if found.
    """
    try:
        # Standardize URL
        if not pin_url.startswith("http"):
            pin_url = f"{settings.PINTEREST_BASE_URL}{pin_url}"
            
        with httpx.Client(follow_redirects=True, timeout=settings.REQUEST_TIMEOUT_SECONDS) as client:
            response = client.get(pin_url, headers=get_http_headers())
            
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Look for LD+JSON metadata
        ld_json_scripts = soup.find_all("script", type="application/ld+json")
        for script in ld_json_scripts:
            if script.string:
                try:
                    meta = json.loads(script.string)
                    if isinstance(meta, dict) and meta.get("@type") == "SocialMediaPosting":
                        return PinterestPin(
                            title=meta.get("headline") or meta.get("name") or "Pin Detail",
                            pin_url=pin_url,
                            image_url=meta.get("image") or "",
                            board="Pinterest Reference",
                            description=meta.get("articleBody") or meta.get("text") or "",
                            source=meta.get("sharedContent", {}).get("url") or ""
                        )
                except Exception:
                    pass
                    
        # DOM fallback
        title_meta = soup.find("meta", property="og:title")
        img_meta = soup.find("meta", property="og:image")
        desc_meta = soup.find("meta", property="og:description")
        
        if img_meta and img_meta.get("content"):
            return PinterestPin(
                title=title_meta["content"] if title_meta else "Pin Details",
                pin_url=pin_url,
                image_url=img_meta["content"],
                board="Pinterest Reference",
                description=desc_meta["content"] if desc_meta else "",
                source=""
            )
            
    except Exception as e:
        logger.error(f"Error fetching pin details: {e}")
        
    return None

def get_board_pins(board_url: str, limit: int = 15) -> List[PinterestPin]:
    """
    Fetches lists of pins within a specific board URL.

    Parameters:
        board_url: Direct link to Pinterest board.
        limit: Max pin count to return.

    Returns:
        List[PinterestPin]: Pins found on board.
    """
    try:
        # Standardize URL
        if not board_url.startswith("http"):
            board_url = f"{settings.PINTEREST_BASE_URL}{board_url}"
            
        with httpx.Client(follow_redirects=True, timeout=settings.REQUEST_TIMEOUT_SECONDS) as client:
            response = client.get(board_url, headers=get_http_headers())
            
        if response.status_code != 200:
            return []
            
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Try initial data states
        pws_data_script = soup.find("script", id="__PWS_DATA__")
        if pws_data_script and pws_data_script.string:
            try:
                js_state = json.loads(pws_data_script.string)
                pins = parse_pins_from_json_state(js_state)
                if pins:
                    return pins[:limit]
            except Exception:
                pass
                
        # Parse DOM links fallback
        pins = []
        anchors = soup.find_all("a", href=True)
        for anchor in anchors:
            href = anchor["href"]
            if href.startswith("/pin/"):
                img = anchor.find("img")
                if img and img.get("src"):
                    pin_id = href.split("/")[2]
                    pins.append(PinterestPin(
                        title=img.get("alt") or f"Pin {pin_id}",
                        pin_url=f"https://www.pinterest.com{href}",
                        image_url=img["src"],
                        board="Board pins",
                        description="",
                        source=""
                    ))
                    if len(pins) >= limit:
                        break
        return pins
        
    except Exception as e:
        logger.error(f"Error parsing board pins: {e}")
        
    return []

# ============================================
# AGENT INTERACTION
# ============================================
# Ingests keywords from LLM agent tools and outputs formatted Pydantic collections.

# ============================================
# SECURITY NOTES
# ============================================
# Filter outbound URLs and escape raw script contents to protect agent runners.

# ============================================
# FUTURE ENHANCEMENTS
# ============================================
# Implement dynamic rotating proxies (Bright Data / ScraperAPI) integration.

# ============================================
# FUTURE IMPROVEMENTS
# ============================================
#
# 1. Rotating browser headers manager
# 2. Automated cookie parser helpers
# 3. Dynamic tag extraction algorithms
# 4. Proxy verification testing scripts
#
# ============================================
