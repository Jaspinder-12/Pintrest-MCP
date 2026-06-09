"""
Module: crud.py

Purpose:
SQLAlchemy CRUD operations for database tables.

Dependencies:
- sqlalchemy

Usage:
Imported by API route handlers to perform database queries.

Notes:
Implements basic transaction controls and entity creation helpers.

Future Improvements:
- Dynamic transaction rollback wrappers
- Soft-deletion filters on retrieval operations
"""

from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
import uuid
import numpy as np

from app.db import models

# ============================================
# PURPOSE
# ============================================
# This module implements the database transaction and query layer. It provides
# helpers to fetch, update, and create users, boards, collections, and pins.

# ============================================
# BUSINESS LOGIC
# ============================================

def create_board(db: Session, name: str, description: Optional[str], user_id: uuid.UUID) -> models.Board:
    """
    Creates a new inspiration board.

    Parameters:
        db: Active SQLAlchemy database session.
        name: Name of the board.
        description: Creative brief description.
        user_id: Owner user UUID.

    Returns:
        models.Board ORM instance.

    Notes:
        Future versions should support collaborative editing.
    """
    board = models.Board(
        name=name,
        description=description,
        user_id=user_id
    )
    db.add(board)
    db.commit()
    db.refresh(board)
    return board

def get_board(db: Session, board_id: uuid.UUID) -> Optional[models.Board]:
    """
    Fetches a board by UUID.

    Parameters:
        db: Active database session.
        board_id: Target board UUID.

    Returns:
        Optional[models.Board] instance if found.
    """
    return db.query(models.Board).filter(models.Board.id == board_id).first()

def get_boards_by_user(db: Session, user_id: uuid.UUID) -> List[models.Board]:
    """
    Fetches all boards owned by a specific user.

    Parameters:
        db: Active database session.
        user_id: Owner user UUID.

    Returns:
        List[models.Board]: Owned boards.
    """
    return db.query(models.Board).filter(models.Board.user_id == user_id).all()

def save_pin(db: Session, pin_id: str, title: Optional[str], description: Optional[str], image_url: str, source_url: Optional[str]) -> models.Pin:
    """
    Creates or registers a visual pin.

    Parameters:
        db: Active database session.
        pin_id: Pinterest pin ID or UUID.
        title: Title of visual asset.
        description: Description notes.
        image_url: Image download link.
        source_url: Original site link.

    Returns:
        models.Pin ORM instance.
    """
    pin = db.query(models.Pin).filter(models.Pin.id == pin_id).first()
    if not pin:
        pin = models.Pin(
            id=pin_id,
            title=title,
            description=description,
            image_url=image_url,
            source_url=source_url
        )
        db.add(pin)
        db.commit()
        db.refresh(pin)
    return pin

def add_pin_to_board(db: Session, board_id: uuid.UUID, pin_id: str) -> bool:
    """
    Binds a visual pin reference to a target board.

    Parameters:
        db: Active database session.
        board_id: Target board UUID.
        pin_id: Target pin ID string.

    Returns:
        bool: True if added successfully.
    """
    board = get_board(db, board_id)
    pin = db.query(models.Pin).filter(models.Pin.id == pin_id).first()
    
    if board and pin:
        # Check if already linked
        if pin not in board.pins:
            board.pins.append(pin)
            db.commit()
            db.refresh(board)
            return True
    return False

def update_board_centroid(db: Session, board_id: uuid.UUID, vectors: List[List[float]]) -> Optional[models.Board]:
    """
    Recalculates the vector centroid style of a board based on its pins.

    Parameters:
        db: Active database session.
        board_id: Target board UUID.
        vectors: List of float arrays representing pin embeddings.

    Returns:
        Optional[models.Board]: Updated board object.
    """
    board = get_board(db, board_id)
    if board and vectors:
        # Calculate mathematical average (centroid)
        arr = np.array(vectors)
        centroid = np.mean(arr, axis=0).tolist()
        board.vector_centroid = [float(x) for x in centroid]
        db.commit()
        db.refresh(board)
        return board
    return None

# ============================================
# AGENT INTERACTION
# ============================================
# Agents call these methods through board and pin routing services to maintain 
# session persistent memories.

# ============================================
# SECURITY NOTES
# ============================================
# User ID validation should occur at route controllers prior to executing CRUD queries.

# ============================================
# FUTURE ENHANCEMENTS
# ============================================
# Configure soft deletes utilizing SQLAlchemy event listener hooks.

# ============================================
# FUTURE IMPROVEMENTS
# ============================================
#
# 1. Soft delete filters mapping
# 2. Collaborative board shared member queries
# 3. Dynamic search cache flushing events
# 4. Partitioned queries for pins tables
#
# ============================================
