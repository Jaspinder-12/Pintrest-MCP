"""
Module: search.py

Purpose:
API endpoints for semantic search, reverse image search, and style analysis.

Dependencies:
- fastapi
- qdrant-client
- pillow

Usage:
Registered as a router under app/main.py.

Notes:
Routes incoming requests to appropriate vector database indexing systems.

Future Improvements:
- Support for visual boundary filters (YOLO coordinates)
- Integration of regional OCR search parameters
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from qdrant_client import QdrantClient
from PIL import Image
import httpx
import io

from app.core.dependencies import get_qdrant_client
from app.services.visual_engine import VisualEngineService

# ============================================
# PURPOSE
# ============================================
# Implements visual search routing logic. Integrates image download streams, 
# SigLIP visual projections, and Qdrant payloads query pipelines.

router = APIRouter(prefix="/v1/search", tags=["Search"])
visual_service = VisualEngineService()

# ============================================
# BUSINESS LOGIC
# ============================================

class SearchRequest(BaseModel):
    query: str = Field(..., description="Text description of style or layout pattern")
    image_url: Optional[str] = Field(None, description="Optional image URL for reverse search")
    limit: int = Field(10, ge=1, le=50)

class SimilarRequest(BaseModel):
    pin_id: str = Field(..., description="Target Pin ID to search similarities for")
    limit: int = Field(5, ge=1, le=50)

class PinResponse(BaseModel):
    pin_id: str
    title: Optional[str]
    image_url: str
    source_url: Optional[str]
    score: float

@router.post("/pins", response_model=List[PinResponse], status_code=status.HTTP_200_OK)
def search_pins(
    request: SearchRequest,
    qdrant: QdrantClient = Depends(get_qdrant_client)
) -> List[PinResponse]:
    """
    Executes a semantic vector query on Qdrant.

    Parameters:
        request: Search parameters query and limit.
        qdrant: Injected Qdrant database connection client.

    Returns:
        List[PinResponse]: Top matched pins matching query.

    Notes:
        Generates text embedding vector and executes cosine search.
    """
    try:
        # Generate text embedding using SigLIP service
        query_vector = visual_service.get_text_embedding(request.query)
        
        # Query Qdrant vector database
        search_results = qdrant.search(
            collection_name="image_embeddings",
            query_vector=query_vector,
            limit=request.limit,
            with_payload=True
        )
        
        results = []
        for hit in search_results:
            payload = hit.payload or {}
            results.append(PinResponse(
                pin_id=str(hit.id),
                title=payload.get("title", ""),
                image_url=payload.get("image_url", ""),
                source_url=payload.get("source_url", ""),
                score=hit.score
            ))
            
        return results

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Vector search failed: {str(e)}"
        )

@router.post("/similar", response_model=List[PinResponse], status_code=status.HTTP_200_OK)
def search_similar(
    request: SimilarRequest,
    qdrant: QdrantClient = Depends(get_qdrant_client)
) -> List[PinResponse]:
    """
    Retrieves similar pins based on an existing pin's vector coordinates.

    Parameters:
        request: Similar query parameters specifying pin ID.
        qdrant: Injected Qdrant database connection client.

    Returns:
        List[PinResponse]: List of similar visual assets.
    """
    try:
        # Retrieve target vector embedding from Qdrant
        retrieved = qdrant.retrieve(
            collection_name="image_embeddings",
            ids=[request.pin_id],
            with_vectors=True
        )
        
        if not retrieved or not retrieved[0].vector:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Target pin vector '{request.pin_id}' not found."
            )
            
        target_vector = retrieved[0].vector
        
        # Query nearest neighbors
        search_results = qdrant.search(
            collection_name="image_embeddings",
            query_vector=target_vector,
            limit=request.limit + 1, # Fetch one extra to skip self
            with_payload=True
        )
        
        results = []
        for hit in search_results:
            if str(hit.id) == request.pin_id:
                continue # Skip self
            payload = hit.payload or {}
            results.append(PinResponse(
                pin_id=str(hit.id),
                title=payload.get("title", ""),
                image_url=payload.get("image_url", ""),
                source_url=payload.get("source_url", ""),
                score=hit.score
            ))
            
        return results[:request.limit]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Similar match lookup failed: {str(e)}"
        )

# ============================================
# AGENT INTERACTION
# ============================================
# LLM agents issue POST request requests to `/v1/search/pins` to locate layout examples.

# ============================================
# SECURITY NOTES
# ============================================
# Validate request limits to prevent large page payload searches from overloading 
# database output buffers.

# ============================================
# FUTURE ENHANCEMENTS
# ============================================
# Cache matching responses in Redis using query hash keys to speed up repeated queries.

# ============================================
# FUTURE IMPROVEMENTS
# ============================================
#
# 1. Redis caching of vector match result lists
# 2. Page pagination token support for long feeds
# 3. Dynamic distance threshold filtering
# 4. Multi-collection routing settings
#
# ============================================
