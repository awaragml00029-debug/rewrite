# AWIES Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites

- Python 3.10+
- Node.js 18+
- An LLM API key (OpenAI or Gemini)

## Step 1: Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Configure your API key
cp .env.example .env
# Edit .env and add your LLM API key

# Start the backend (auto-installs dependencies)
./start.sh
```

The backend will start at http://localhost:8000

**Test it:**
```bash
curl http://localhost:8000/api/health
```

## Step 2: Frontend Setup (2 minutes)

Open a new terminal:

```bash
# Navigate to frontend
cd frontend

# Start the frontend (auto-installs dependencies)
./start.sh
```

The frontend will open at http://localhost:3000

## Step 3: Use AWIES! (1 minute)

1. Open http://localhost:3000 in your browser
2. Paste some text (e.g., "This is a big problem in research.")
3. Click **Analyze** to see quality analysis
4. Click **Enhance** to improve the text
5. View the **Compare** tab to see changes
6. Export your enhanced text!

## Configuration Options

### Using OpenAI (default)

```env
# In backend/.env
LLM_PROVIDER=openai
LLM_API_KEY=sk-your-key-here
LLM_MODEL=gpt-4
```

### Using Google Gemini

```env
# In backend/.env
LLM_PROVIDER=gemini
LLM_API_KEY=your-gemini-key
LLM_MODEL=gemini-pro
```

### Using Local Models

```env
# In backend/.env
LLM_PROVIDER=openai
LLM_BASE_URL=http://localhost:1234/v1
LLM_API_KEY=not-needed
LLM_MODEL=local-model-name
```

## Enhancement Levels

- **Level 1** - Basic grammar and spelling corrections (fastest)
- **Level 2** - Native-like expressions and collocations
- **Level 3** - Academic style and formal vocabulary
- **Level 4** - Complete discourse optimization (slowest)

## Supported Disciplines

- General (default)
- Computer Science
- Biology
- Social Sciences
- Engineering

Each discipline has specific writing conventions.

## API Examples

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
# Create enhancement job
curl -X POST "http://localhost:8000/api/enhance" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "We need to make research on this topic.",
    "level": 2,
    "discipline": "general"
  }'

# Response: {"job_id": "...", "status": "pending"}

# Check status
curl "http://localhost:8000/api/enhance/status/{job_id}"
```

### Get Journal Recommendations

```bash
curl -X POST "http://localhost:8000/api/recommendations/journals" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Machine learning in medical diagnosis...",
    "limit": 10
  }'
```

## Troubleshooting

### Backend Won't Start

1. Check Python version: `python --version` (need 3.10+)
2. Check API key in `.env`
3. Install manually: `pip install -r requirements.txt`

### Frontend Won't Start

1. Check Node version: `node --version` (need 18+)
2. Clear and reinstall: `rm -rf node_modules && npm install`
3. Check backend is running on port 8000

### "Analysis failed" Error

- Check your LLM API key is valid
- Check you have credits/quota
- Try a shorter text first

### JANE Recommendations Empty

- JANE API may be temporarily unavailable
- This won't affect the core enhancement features

## Performance Tips

✅ **Use Level 1-2 for faster processing** (5-10 seconds)
✅ **Enable caching** for repeated requests
✅ **Use local models** for unlimited usage
✅ **Break long texts** into paragraphs

## What's Next?

- 📚 Read the full documentation in `AWIES_Complete_Design_Document.md`
- 🔧 Customize discipline-specific rules
- 🚀 Deploy to production with Docker
- 📊 Add custom analysis metrics

## Need Help?

- Backend API docs: http://localhost:8000/docs
- Frontend README: `frontend/README.md`
- Backend README: `backend/README.md`
- Full design doc: `AWIES_Complete_Design_Document.md`

---

**Enjoy improving your academic writing! 🎓✨**
