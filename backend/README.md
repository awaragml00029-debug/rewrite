# AWIES Backend

Academic Writing Intelligence Enhancement System - Backend API

## Features

- ✅ **Multi-level Text Enhancement** (4 levels from basic corrections to discourse optimization)
- ✅ **Comprehensive Text Analysis** (lexical, syntactic, discourse)
- ✅ **LLM Integration** (OpenAI and Gemini API support)
- ✅ **JANE API Integration** (journal, paper, and author recommendations)
- ✅ **Async Processing** with progress tracking
- ✅ **RESTful API** with automatic documentation

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Choose your LLM provider
LLM_PROVIDER=openai  # or "gemini"
LLM_API_KEY=your-api-key-here
LLM_MODEL=gpt-4  # or "gemini-pro"

# Optional: Custom base URL (for local models, Azure, etc.)
# LLM_BASE_URL=https://api.openai.com/v1
```

### 3. Run the Server

```bash
# Development mode
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access API Documentation

Open your browser:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Text Analysis
```bash
POST /api/analyze
```
Analyze text for quality issues.

### Text Enhancement
```bash
# Create enhancement job
POST /api/enhance

# Check status
GET /api/enhance/status/{job_id}
```

### Recommendations
```bash
# Get journal recommendations
POST /api/recommendations/journals

# Get related papers
POST /api/recommendations/papers

# Get author recommendations
POST /api/recommendations/authors
```

## Example Usage

### Analyze Text

```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is a big problem in modern research.",
    "discipline": "computer_science"
  }'
```

### Enhance Text

```bash
# Create job
curl -X POST "http://localhost:8000/api/enhance" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "We need to make research on this topic.",
    "level": 2,
    "discipline": "general"
  }'

# Returns: {"job_id": "xxx", "status": "pending"}

# Check status
curl "http://localhost:8000/api/enhance/status/xxx"
```

### Get Recommendations

```bash
curl -X POST "http://localhost:8000/api/recommendations/journals" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Machine learning applications in healthcare...",
    "limit": 10
  }'
```

## Configuration

### LLM Providers

#### OpenAI (default)
```env
LLM_PROVIDER=openai
LLM_API_KEY=sk-...
LLM_MODEL=gpt-4
```

#### Google Gemini
```env
LLM_PROVIDER=gemini
LLM_API_KEY=your-gemini-key
LLM_MODEL=gemini-pro
```

#### Local Models (OpenAI-compatible)
```env
LLM_PROVIDER=openai
LLM_BASE_URL=http://localhost:1234/v1
LLM_API_KEY=not-needed
LLM_MODEL=local-model
```

### Enhancement Levels

1. **Level 1**: Basic grammar and spelling corrections
2. **Level 2**: Native-like expression improvements
3. **Level 3**: Academic style and conventions
4. **Level 4**: Overall discourse optimization

### Discipline Support

- `computer_science`
- `biology`
- `social_sciences`
- `engineering`
- `general` (default)

## Architecture

```
backend/
├── app/
│   ├── api/          # API routes
│   ├── core/         # Configuration
│   ├── services/     # Business logic
│   │   ├── llm_client.py         # LLM integration
│   │   ├── text_analyzer.py      # Text analysis
│   │   ├── enhancement_engine.py # Enhancement logic
│   │   └── jane_client.py        # JANE API
│   ├── models/       # Pydantic schemas
│   └── main.py       # FastAPI app
├── tests/            # Unit tests
└── requirements.txt
```

## Development

### Run Tests
```bash
pytest tests/
```

### Code Quality
```bash
# Format code
black app/

# Lint
flake8 app/

# Type check
mypy app/
```

## Troubleshooting

### LLM API Errors
- Check your API key is valid
- Verify you have credits/quota
- Check the base URL is correct

### JANE API Not Working
- JANE API may be temporarily unavailable
- The system will gracefully degrade and return empty recommendations

### Performance Issues
- Use Level 1-2 for faster processing
- Enable Redis caching for repeated requests
- Consider using local LLM models

## License

MIT License
