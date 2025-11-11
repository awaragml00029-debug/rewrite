# AWIES - Academic Writing Intelligence Enhancement System

🎓 Professional academic writing enhancement system with AI-powered text improvement and literature recommendations.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](docker-compose.yml)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/react-18+-blue.svg)](https://reactjs.org/)

[中文文档](README_CN.md) | **English**

## ✨ Features

- 🎯 **4-Level Text Enhancement** - Progressive AI-powered improvements
  - Level 1: Grammar and spelling corrections
  - Level 2: Natural expression improvements
  - Level 3: Academic style and conventions
  - Level 4: Discourse optimization and flow

- 📊 **Comprehensive Text Analysis**
  - Lexical diversity and vocabulary assessment
  - Syntactic complexity analysis
  - Discourse coherence evaluation

- 📚 **Literature Recommendations** (via JANE API)
  - Relevant paper suggestions with DOI links
  - Author/collaborator recommendations
  - PubMed integration

- 🔍 **Side-by-Side Comparison** - Detailed diff view with change tracking
- 🎨 **Modern UI** - Clean, responsive interface
- 🚫 **Anti-AI Detection** - Maintains human writing characteristics
- 🐳 **Docker Ready** - One-command deployment

## 🚀 Quick Start with Docker (Recommended)

### Prerequisites
- Docker 20.10+ and Docker Compose 2.0+
- OpenAI or Gemini API key

### Installation

```bash
# 1. Copy environment template
cp .env.docker.example .env

# 2. Edit .env and add your API credentials
nano .env

# 3. Start services
./docker-start.sh

# Or manually:
docker-compose up -d
```

Access the application:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

📖 See [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for detailed Docker documentation.

## ⚙️ Configuration

### OpenAI Setup
```bash
LLM_PROVIDER=openai
LLM_API_KEY=sk-your-key-here
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o
```

### Google Gemini Setup
```bash
LLM_PROVIDER=gemini
LLM_API_KEY=your-gemini-key
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta
LLM_MODEL=gemini-2.0-flash-001
```

### OpenAI-Compatible APIs
```bash
LLM_PROVIDER=openai
LLM_API_KEY=your-key
LLM_BASE_URL=https://api.ohmygpt.com/v1
LLM_MODEL=gpt-4o
```

## 📖 Usage

1. **Enter Text** - Paste academic text (up to 4000 characters)
2. **Select Options** - Choose discipline and enhancement level
3. **Enhance** - Click enhance button
4. **Review** - Compare original and enhanced text
5. **Copy** - Use quick copy button for enhanced text

### Enhancement Levels

| Level | Name | Function | Use Case |
|-------|------|----------|----------|
| 1 | Basic | Grammar & spelling | Draft stage |
| 2 | Expression | Natural phrasing | Fluency improvement |
| 3 | Academic | Formal style | Publication prep |
| 4 | Discourse | Flow & structure | Final polish |

## 🏗️ Manual Installation

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Configure
cp .env.example .env
nano .env  # Add API key

# Start
./start.sh
```

### Frontend

```bash
cd frontend

# Install and start
npm install
npm run dev
```

## 📚 API Documentation

### Key Endpoints

- `POST /api/analyze` - Analyze text quality
- `POST /api/enhance` - Create enhancement job
- `GET /api/enhance/status/{job_id}` - Check status
- `POST /api/recommendations/papers` - Get paper suggestions
- `POST /api/recommendations/authors` - Get author suggestions

Full API docs: http://localhost:8000/docs

## 🛠️ Tech Stack

**Backend**
- FastAPI - Modern Python web framework
- OpenAI/Gemini - LLM integration
- spaCy, NLTK - NLP processing
- JANE API - Literature recommendations

**Frontend**
- React 18 + TypeScript
- Ant Design - UI components
- Monaco Editor - Text editing
- Vite - Build tool

## 🐳 Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild
docker-compose up -d --build

# Check status
docker-compose ps
```

## 🔧 Troubleshooting

**Empty enhancement results**
- Verify API key is correct
- Check model name matches provider
- View logs: `docker-compose logs backend`

**Slow enhancement**
- Normal for long texts (1000+ chars)
- Level 4 takes longest
- Check API rate limits

**Port conflicts**
- Change ports in `.env`:
  ```bash
  BACKEND_PORT=8001
  FRONTEND_PORT=3001
  ```

See [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for more troubleshooting.

## 📁 Project Structure

```
rewrite/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Configuration
│   │   ├── services/     # Business logic
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/             # React frontend
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── hooks/        # Custom hooks
│   │   └── services/     # API services
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml    # Docker orchestration
├── docker-start.sh       # Quick start script
└── DOCKER_DEPLOYMENT.md  # Docker docs
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Credits

- Text enhancement: OpenAI/Gemini APIs
- Literature recommendations: JANE API
- UI framework: Ant Design
- Built with: FastAPI, React, TypeScript

## 📞 Support

- 📖 [Docker Documentation](DOCKER_DEPLOYMENT.md)
- 🐛 [Report Issues](https://github.com/your-repo/issues)
- 💬 [Discussions](https://github.com/your-repo/discussions)

---

Made with ❤️ for academic researchers worldwide
