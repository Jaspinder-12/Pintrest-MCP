"""
Module: config.py

Purpose:
Application settings configuration parsed from environment variables.

Dependencies:
pydantic-settings

Usage:
Imported across modules to load settings variables.

Notes:
Validates environment parameters.

Future Improvements:
- HashiCorp Vault integrations
- Dynamic reloading configuration setups
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

# ============================================
# PURPOSE
# ============================================
# This module implements the unified Configuration management system for the 
# FastAPI core server. It leverages Pydantic-Settings to validate environment 
# variables at startup, preventing initialization in broken states (Fail-Fast).

# ============================================
# BUSINESS LOGIC
# ============================================
class Settings(BaseSettings):
    """
    Main Settings configurations model parsing .env files.
    """
    # General Options
    ENV: str = "production"
    DEBUG: bool = False
    PROJECT_NAME: str = "Pinterest MCP Core API"
    LOG_LEVEL: str = "INFO"

    # Database URLs
    DATABASE_URL: str = "postgresql://mcp_user:mcp_password@localhost:5432/pinterest_mcp_dev"
    REDIS_URL: str = "redis://localhost:6379/0"
    QDRANT_URL: str = "http://localhost:6333"
    
    # Model Configurations
    MODEL_CACHE_DIR: str = "/app/models/cache"
    CLIP_MODEL_NAME: str = "siglip-so400m-patch14-384"

    # Pydantic Settings Config Model
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

def get_settings() -> Settings:
    """
    Instantiates settings mapping.

    Parameters:
        None.

    Returns:
        Settings: Config class mapping environment variables.

    Notes:
        Settings is returned as an initialized model.
    """
    return Settings()

# ============================================
# AGENT INTERACTION
# ============================================
# AI agents can read this config settings class to check available configurations 
# and env names required for database connections.

# ============================================
# SECURITY NOTES
# ============================================
# Sensitive database URLs and credential tokens must be supplied via 
# environment variables or vaults. Do not hardcode real values inside 
# default settings strings.

# ============================================
# FUTURE ENHANCEMENTS
# ============================================
# Add KMS decrypt wrapper layers for secret string variables.

# ============================================
# FUTURE IMPROVEMENTS
# ============================================
#
# 1. Multi-user tenant database configurations
# 2. Dynamic config change polling hooks
# 3. Parameter validation checks for model paths
# 4. Strict type casting logic mappings
#
# ============================================
