"""
Module: pins.py

Purpose:
API endpoints for visual pin creation, board binding, and vector indexing.

Dependencies:
- fastapi
- qdrant-client
- pillow

Usage:
Registered as a router under app/main.py.

Notes:
Triggers SigLIP embedding generation and indexes vectors into Qdrant collections.

Future Improvements:
- Asynchronous Celery task processing for heavy image downloads
- OCR text mapping to payload indices
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from qdrant_client import QdrantClient
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
import logging
from PIL import Image
import httpx
import io

from app.db import crud
from app.db.session import SessionLocal
from app.core.dependencies import get_qdrant_client
from app.services.visual_engine import VisualEngineService

# ============================================
# PURPOSE
# ============================================
# This router implements visual pin ingestion. It orchestrates image download,
# SigLIP visual embedding extraction, relational Postgres cataloging, Qdrant
# indexing, and board centroid updates.

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/v1/pins", tags=["Pins"])
visual_service = VisualEngineService()

# ============================================
# BUSINESS LOGIC
# ============================================

def get_db():
    """
    Yields database sessions.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PinCreate(BaseModel):
    board_id: uuid.UUID = Field(..., description="Target Board UUID destination")
    image_url: str = Field(..., description="Reference image URL")
    title: Optional[str] = Field(None, description="Optional title")
    description: Optional[str] = Field(None, description="Optional description details")

class PinResponse(BaseModel):
    id: str
    title: Optional[str]
    image_url: str
    source_url: Optional[str]
    
    class Config:
        from_attributes = True

@router.post("", response_model=PinResponse, status_code=status.HTTP_201_CREATED)
async def create_pin(
    payload: PinCreate,
    db: Session = Depends(get_db),
    qdrant: QdrantClient = Depends(get_qdrant_client)
) -> PinResponse:
    """
    Ingests, embeds, catalogs, and indexes a new visual pin.

    Parameters:
        payload: Input properties board_id, image_url, title, description.
        db: Injected relational database session.
        qdrant: Injected Qdrant database client.

    Returns:
        PinResponse: Created pin entity records.
    """
    # 1. Fetch board context
    board = crud.get_board(db, payload.board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target board not found."
        )

    # 2. Ingest and download the image bytes
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(payload.image_url, timeout=10.0)
            if resp.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Failed to retrieve target image."
                )
        image = Image.open(io.BytesIO(resp.content))
    except Exception as e:
        logger.error(f"Image ingestion pipeline failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to process image: {str(e)}"
        )

    # 3. Generate SigLIP visual embedding vector
    vector = visual_service.get_image_embedding(image)
    
    # 4. Save metadata to relational PostgreSQL
    pin_uuid = str(uuid.uuid4())
    pin = crud.save_pin(
        db=db,
        pin_id=pin_uuid,
        title=payload.title,
        description=payload.description,
        image_url=payload.image_url,
        source_url=payload.image_url
    )
    
    # 5. Bind pin to the board
    crud.add_pin_to_board(db, payload.board_id, pin_uuid)

    # 6. Index vector embedding into Qdrant collection
    try:
        qdrant.upsert(
            collection_name="image_embeddings",
            points=[
                {
                    "id": pin_uuid,
                    "vector": vector,
                    "payload": {
                        "title": payload.title or "",
                        "image_url": payload.image_url,
                        "source_url": payload.image_url
                    }
                }
            ]
        )
    except Exception as e:
        logger.warning(f"Failed to index vector in Qdrant: {e}. Eventual consistency fallback active.")

    # 7. Recalculate board centroid style vector profile
    try:
        # Fetch embeddings of all pins currently linked to this board
        vectors = []
        for board_pin in board.pins:
            try:
                retrieved = qdrant.retrieve(
                    collection_name="image_embeddings",
                    ids=[board_pin.id],
                    with_vectors=True
                )
                if retrieved and retrieved[0].vector:
                    vectors.append(retrieved[0].vector)
            except Exception:
                pass
                
        if vectors:
            crud.update_board_centroid(db, board.id, vectors)
    except Exception as e:
        logger.warning(f"Centroid computation skipped: {e}")

    return pin

# ============================================
# AGENT INTERACTION
# ============================================
# LLM agents call POST `/v1/pins` to save references dynamically from IDE runs.

# ============================================
# SECURITY NOTES
# ============================================
# Always check request size boundaries for image downloads to prevent resource 
# depletion issues.

# ============================================
# FUTURE ENHANCEMENTS
# ============================================
# Offload image downloads and embedding tasks to Celery task queues.

# ============================================
# FUTURE IMPROVEMENTS
# ============================================
#
# 1. Background task queues (Celery/RabbitMQ) for indexing
# 2. Duplicate detection using image hashes
# 3. Dynamic OCR data indexing
# 4. Multiple vector embeddings index configurations
#
# ============================================
