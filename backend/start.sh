#!/bin/bash

# AWIES Backend Start Script

echo "================================"
echo "Starting AWIES Backend Server"
echo "================================"

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Copying .env.example to .env..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys!"
    echo ""
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Download spaCy model if needed
echo "📚 Checking spaCy models..."
python -c "import spacy; spacy.load('en_core_web_sm')" 2>/dev/null || {
    echo "📥 Downloading spaCy English model..."
    python -m spacy download en_core_web_sm
}

# Download NLTK data if needed
echo "📚 Checking NLTK data..."
python -c "import nltk; nltk.data.find('tokenizers/punkt')" 2>/dev/null || {
    echo "📥 Downloading NLTK data..."
    python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"
}

# Start server
echo ""
echo "🚀 Starting server..."
echo "📖 API Documentation: http://localhost:8000/docs"
echo "❤️  Health Check: http://localhost:8000/api/health"
echo ""
python -m app.main
