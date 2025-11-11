"""Pydantic models for request/response validation."""

from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field


# Request Models
class AnalyzeRequest(BaseModel):
    """Request model for text analysis."""
    text: str = Field(..., min_length=10, description="Text to analyze")
    discipline: str = Field(default="general", description="Academic discipline")
    analysis_types: List[str] = Field(
        default=["lexical", "syntactic", "discourse"],
        description="Types of analysis to perform"
    )


class EnhanceRequest(BaseModel):
    """Request model for text enhancement."""
    text: str = Field(..., min_length=10, description="Text to enhance")
    level: int = Field(..., ge=1, le=4, description="Enhancement level (1-4)")
    discipline: str = Field(default="general", description="Academic discipline")
    options: Dict[str, Any] = Field(default_factory=dict, description="Additional options")


class RecommendationRequest(BaseModel):
    """Request model for recommendations."""
    text: str = Field(..., min_length=20, description="Text for recommendations")
    filters: Optional[str] = Field(default="", description="Optional filters")
    limit: int = Field(default=10, ge=1, le=50, description="Number of results")


# Response Models
class AnalysisResponse(BaseModel):
    """Response model for text analysis."""
    overall_score: int
    lexical: Dict[str, Any]
    syntactic: Dict[str, Any]
    discourse: Dict[str, Any]
    statistics: Dict[str, Any]


class EnhancementJobResponse(BaseModel):
    """Response model for enhancement job creation."""
    job_id: str
    status: str
    message: str


class EnhancementStatusResponse(BaseModel):
    """Response model for enhancement status."""
    status: Literal["pending", "processing", "completed", "failed"]
    progress: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class EnhancementResult(BaseModel):
    """Model for enhancement result."""
    enhanced_text: str
    changes: List[Dict[str, Any]]
    report: Dict[str, Any]


class JournalRecommendation(BaseModel):
    """Model for journal recommendation."""
    title: str
    similarity_score: float
    impact_factor: Optional[float] = None
    open_access: bool
    publisher: str
    url: str
    confidence: str


class PaperRecommendation(BaseModel):
    """Model for paper recommendation."""
    title: str
    authors: List[str]
    year: Optional[int] = None
    journal: str
    doi: str
    similarity_score: float
    citations: Optional[int] = None
    url: str


class AuthorRecommendation(BaseModel):
    """Model for author recommendation."""
    name: str
    affiliation: str
    h_index: Optional[int] = None
    total_publications: int
    similarity_score: float


class JournalRecommendationsResponse(BaseModel):
    """Response model for journal recommendations."""
    journals: List[JournalRecommendation]


class PaperRecommendationsResponse(BaseModel):
    """Response model for paper recommendations."""
    papers: List[PaperRecommendation]


class AuthorRecommendationsResponse(BaseModel):
    """Response model for author recommendations."""
    authors: List[AuthorRecommendation]


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: str
    version: str = "1.0.0"
