"""Basic API tests."""

import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


@pytest.mark.asyncio
async def test_analyze_text():
    """Test text analysis endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/analyze",
            json={
                "text": "This is a big problem in modern research. We need to find good solutions.",
                "discipline": "computer_science"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "overall_score" in data
        assert "lexical" in data
        assert "syntactic" in data
        assert "discourse" in data
        assert "statistics" in data


@pytest.mark.asyncio
async def test_enhance_text():
    """Test text enhancement endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create enhancement job
        response = await client.post(
            "/api/enhance",
            json={
                "text": "This is a test. We need to make research.",
                "level": 1,
                "discipline": "general"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data
        assert data["status"] == "pending"

        # Check job status
        job_id = data["job_id"]
        status_response = await client.get(f"/api/enhance/status/{job_id}")
        assert status_response.status_code == 200
        status_data = status_response.json()
        assert "status" in status_data


@pytest.mark.asyncio
async def test_invalid_text_too_short():
    """Test validation for text that's too short."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/analyze",
            json={
                "text": "Short",
                "discipline": "general"
            }
        )
        assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_invalid_enhancement_level():
    """Test validation for invalid enhancement level."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/enhance",
            json={
                "text": "This is a test text for enhancement.",
                "level": 5,  # Invalid: max is 4
                "discipline": "general"
            }
        )
        assert response.status_code == 422  # Validation error
