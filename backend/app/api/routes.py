"""API routes for AWIES backend."""

import logging
import uuid
from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks

from app.models.schemas import (
    AnalyzeRequest,
    AnalysisResponse,
    EnhanceRequest,
    EnhancementJobResponse,
    EnhancementStatusResponse,
    RecommendationRequest,
    JournalRecommendationsResponse,
    PaperRecommendationsResponse,
    AuthorRecommendationsResponse,
    HealthResponse
)
from app.services.text_analyzer import TextAnalyzer
from app.services.enhancement_engine import EnhancementEngine
from app.services.jane_client import JANEClient

logger = logging.getLogger(__name__)

router = APIRouter()

# In-memory job storage (in production, use Redis or database)
enhancement_jobs: Dict[str, Dict[str, Any]] = {}


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_text(request: AnalyzeRequest):
    """
    Analyze text for quality issues.

    Performs lexical, syntactic, and discourse analysis.
    """
    try:
        logger.info(f"Analyzing text: {len(request.text)} characters")

        analyzer = TextAnalyzer()
        result = await analyzer.analyze(request.text, request.discipline)

        return result

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/enhance", response_model=EnhancementJobResponse)
async def create_enhancement_job(
    request: EnhanceRequest,
    background_tasks: BackgroundTasks
):
    """
    Create an enhancement job.

    Returns a job ID that can be used to check status and retrieve results.
    """
    try:
        # Generate job ID
        job_id = str(uuid.uuid4())

        # Initialize job status
        enhancement_jobs[job_id] = {
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "progress": None,
            "result": None,
            "error": None
        }

        # Start enhancement in background
        background_tasks.add_task(
            process_enhancement,
            job_id,
            request.text,
            request.level,
            request.discipline
        )

        logger.info(f"Created enhancement job: {job_id}")

        return {
            "job_id": job_id,
            "status": "pending",
            "message": "Enhancement job created successfully"
        }

    except Exception as e:
        logger.error(f"Failed to create enhancement job: {e}")
        raise HTTPException(status_code=500, detail=f"Job creation failed: {str(e)}")


@router.get("/enhance/status/{job_id}", response_model=EnhancementStatusResponse)
async def get_enhancement_status(job_id: str):
    """
    Get the status of an enhancement job.

    Returns the current status and results if complete.
    """
    if job_id not in enhancement_jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = enhancement_jobs[job_id]

    return {
        "status": job["status"],
        "progress": job.get("progress"),
        "result": job.get("result"),
        "error": job.get("error")
    }


async def process_enhancement(
    job_id: str,
    text: str,
    level: int,
    discipline: str
):
    """
    Process enhancement job in background.

    Updates job status and stores results.
    """
    try:
        # Update status
        enhancement_jobs[job_id]["status"] = "processing"

        # Create enhancement engine
        engine = EnhancementEngine()

        # Progress callback
        def update_progress(progress_data: Dict[str, Any]):
            enhancement_jobs[job_id]["progress"] = progress_data

        # Perform enhancement
        result = await engine.enhance(
            text=text,
            level=level,
            discipline=discipline,
            progress_callback=update_progress
        )

        # Store result
        enhancement_jobs[job_id]["status"] = "completed"
        enhancement_jobs[job_id]["result"] = result

        logger.info(f"Enhancement job {job_id} completed successfully")

    except Exception as e:
        logger.error(f"Enhancement job {job_id} failed: {e}")
        enhancement_jobs[job_id]["status"] = "failed"
        enhancement_jobs[job_id]["error"] = str(e)


@router.post("/recommendations/journals", response_model=JournalRecommendationsResponse)
async def get_journal_recommendations(request: RecommendationRequest):
    """
    Get journal recommendations based on text.

    Uses JANE API to find suitable journals.
    """
    try:
        logger.info("Getting journal recommendations")

        jane_client = JANEClient()
        journals = await jane_client.get_journal_recommendations(
            text=request.text,
            filter_string=request.filters,
            limit=request.limit
        )

        return {"journals": journals}

    except Exception as e:
        logger.error(f"Failed to get journal recommendations: {e}")
        # Return empty list instead of error to allow graceful degradation
        return {"journals": []}


@router.post("/recommendations/papers", response_model=PaperRecommendationsResponse)
async def get_paper_recommendations(request: RecommendationRequest):
    """
    Get related paper recommendations based on text.

    Uses JANE API to find relevant papers.
    """
    try:
        logger.info("Getting paper recommendations")

        jane_client = JANEClient()
        papers = await jane_client.find_related_papers(
            text=request.text,
            count=request.limit,
            filter_string=request.filters
        )

        return {"papers": papers}

    except Exception as e:
        logger.error(f"Failed to get paper recommendations: {e}")
        return {"papers": []}


@router.post("/recommendations/authors", response_model=AuthorRecommendationsResponse)
async def get_author_recommendations(request: RecommendationRequest):
    """
    Get author/collaborator recommendations based on text.

    Uses JANE API to find potential collaborators.
    """
    try:
        logger.info("Getting author recommendations")

        jane_client = JANEClient()
        authors = await jane_client.find_potential_collaborators(
            text=request.text,
            filter_string=request.filters,
            limit=request.limit
        )

        return {"authors": authors}

    except Exception as e:
        logger.error(f"Failed to get author recommendations: {e}")
        return {"authors": []}


@router.delete("/enhance/{job_id}")
async def delete_enhancement_job(job_id: str):
    """Delete an enhancement job and its results."""
    if job_id in enhancement_jobs:
        del enhancement_jobs[job_id]
        return {"message": "Job deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Job not found")
