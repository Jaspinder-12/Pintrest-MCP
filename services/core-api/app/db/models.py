"""
Module: models.py

Purpose:
SQLAlchemy relational models defining metadata tables.

Dependencies:
- sqlalchemy

Usage:
Imported by repositories, services, and migration tools.

Notes:
Implements foreign key constraints and standard index mappings.

Future Improvements:
- Dynamic schema versioning metadata tables
- Encrypted data fields for session tokens
"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Table, Integer, Numeric, Boolean, JSON, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.db.session import Base

# ============================================
# PURPOSE
# ============================================
# This module defines the complete relational schema mapping using SQLAlchemy ORM.
# It includes users, agent sessions, board configurations, pin metadata, and search history tables.

# ============================================
# BUSINESS LOGIC
# ============================================

# Junction table mapping boards to collections
collection_boards = Table(
    "collection_boards",
    Base.metadata,
    Column("collection_id", UUID(as_uuid=True), ForeignKey("collections.id", ondelete="CASCADE"), primary_key=True),
    Column("board_id", UUID(as_uuid=True), ForeignKey("boards.id", ondelete="CASCADE"), primary_key=True)
)

# Junction table mapping pins to boards
board_pins = Table(
    "board_pins",
    Base.metadata,
    Column("board_id", UUID(as_uuid=True), ForeignKey("boards.id", ondelete="CASCADE"), primary_key=True),
    Column("pin_id", String(100), ForeignKey("pins.id", ondelete="CASCADE"), primary_key=True),
    Column("added_at", DateTime(timezone=True), default=datetime.utcnow)
)

class User(Base):
    """
    User account credentials and lifecycle metadata.
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    agents = relationship("Agent", back_populates="user", cascade="all, delete-orphan")
    boards = relationship("Board", back_populates="user", cascade="all, delete-orphan")
    collections = relationship("Collection", back_populates="user", cascade="all, delete-orphan")


class Agent(Base):
    """
    Agent sessions registering unique configurations and allowed permissions.
    """
    __tablename__ = "agents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    agent_name = Column(String(100), nullable=False)
    session_token = Column(String(255), unique=True, nullable=True)
    permissions = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    user = relationship("User", back_populates="agents")
    searches = relationship("Search", back_populates="agent")
    recommendations = relationship("Recommendation", back_populates="agent", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="agent")


class Board(Base):
    """
    Boards representing logical groups of pins.
    """
    __tablename__ = "boards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    vector_centroid = Column(ARRAY(Numeric), nullable=True) # Averaged 768-d vector
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="boards")
    pins = relationship("Pin", secondary=board_pins, back_populates="boards")


class Pin(Base):
    """
    Pin visual references.
    """
    __tablename__ = "pins"

    id = Column(String(100), primary_key=True)
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    image_url = Column(Text, nullable=False)
    source_url = Column(Text, nullable=True)
    aesthetic_score = Column(Numeric(4, 3), default=0.500)
    colors = Column(ARRAY(String(7)), default=list) # List of primary hex values
    metadata_json = Column(JSON, name="metadata", default=dict) # OCR text, layouts, bounding boxes
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    boards = relationship("Board", secondary=board_pins, back_populates="pins")
    recommendations = relationship("Recommendation", back_populates="pin", cascade="all, delete-orphan")


class Collection(Base):
    """
    Collection folders grouping multiple boards.
    """
    __tablename__ = "collections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    user = relationship("User", back_populates="collections")
    boards = relationship("Board", secondary=collection_boards)


class Search(Base):
    """
    Agent query search history.
    """
    __tablename__ = "searches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), nullable=True)
    search_query = Column(Text, nullable=True)
    parsed_filters = Column(JSON, default=dict)
    results_returned_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    agent = relationship("Agent", back_populates="searches")


class Trend(Base):
    """
    Weekly compiled visual trends.
    """
    __tablename__ = "trends"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trend_name = Column(String(255), unique=True, nullable=False)
    vertical = Column(String(100), nullable=False)
    growth_score = Column(Numeric(6, 2), nullable=False)
    signature_colors = Column(ARRAY(String(7)), default=list)
    last_updated = Column(DateTime(timezone=True), default=datetime.utcnow)


class Recommendation(Base):
    """
    Style recommendation cards pushed to agents.
    """
    __tablename__ = "recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    pin_id = Column(String(100), ForeignKey("pins.id", ondelete="CASCADE"), nullable=False)
    score = Column(Numeric(4, 3), nullable=False)
    seen = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    agent = relationship("Agent", back_populates="recommendations")
    pin = relationship("Pin", back_populates="recommendations")


class AuditLog(Base):
    """
    Security audit trails tracking tool invocations.
    """
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), nullable=True)
    action_type = Column(String(100), nullable=False)
    target_resource = Column(String(255), nullable=False)
    payload = Column(JSON, default=dict)
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    agent = relationship("Agent", back_populates="audit_logs")

# ============================================
# AGENT INTERACTION
# ============================================
# Agents use these models via SQLAlchemy repositories.

# ============================================
# SECURITY NOTES
# ============================================
# Cascade deletes are restricted where metadata must remain for audit safety (SET NULL on audit_logs).

# ============================================
# FUTURE ENHANCEMENTS
# ============================================
# Add standard soft-delete flags for boards.

# ============================================
# FUTURE IMPROVEMENTS
# ============================================
#
# 1. Soft-delete flags implementation
# 2. Database partitioning rules for audit_logs
# 3. Model validation validation decorators
# 4. Multi-tenant database routing support
#
# ============================================
