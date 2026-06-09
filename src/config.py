"""
Module: config.py

Purpose:
Application settings and configurations.

Dependencies:
pydantic-settings

Usage:
Imported in scraper and server modules to retrieve connection variables.

Notes:
Uses standard environment variable fallbacks.

Future Improvements:
- Dynamic HTTP User-Agent rotation list
- Key Vault integrations for proxy credentials
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

# ============================================
# PURPOSE
# ============================================
# Manages configuration parameters like base Pinterest URLs, HTTP client timeouts,
# and browser-like request headers to ensure stable HTML scraping rates.

# ============================================
# BUSINESS LOGIC
# ============================================
class Settings(BaseSettings):
    """
    Settings model for loading configurations from environment variables.
    """
    # Environment mode
    ENV: str = "development"
    
    # Pinterest Base URL
    PINTEREST_BASE_URL: str = "https://www.pinterest.com"
    
    # Request configurations
    REQUEST_TIMEOUT_SECONDS: float = 10.0
    
    # Request Headers to mimic mobile safari to trigger pre-rendering
    USER_AGENT: str = (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

def get_settings() -> Settings:
    """
    Retrieves and instantiates the global configuration settings.

    Parameters:
        None.

    Returns:
        Settings: Initialized configuration options model.

    Notes:
        Default configurations are returned.
    """
    return Settings()

# ============================================
# AGENT INTERACTION
# ============================================
# Agents inspect this module signature to discover default timeouts and URL targets.

# ============================================
# SECURITY NOTES
# ============================================
# Keep private tokens or proxy passwords out of default settings parameters.

# ============================================
# FUTURE ENHANCEMENTS
# ============================================
# Add proxy list parser and rotation methods.

# ============================================
# FUTURE IMPROVEMENTS
# ============================================
#
# 1. Rotational User-Agent collection manager
# 2. Automated rate-limiting threshold adapters
# 3. Proxy string parser utilities
# 4. Multi-tenant configuration support
#
# ============================================
