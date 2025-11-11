#!/bin/bash

# AWIES Docker Deployment Script
# ================================

set -e

echo "🚀 AWIES Docker Deployment"
echo "=========================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found"
    echo "📋 Creating .env from template..."
    cp .env.docker.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file and add your API credentials:"
    echo "   - LLM_PROVIDER (openai or gemini)"
    echo "   - LLM_API_KEY (your API key)"
    echo "   - LLM_MODEL (e.g., gpt-4o or gemini-2.0-flash-001)"
    echo ""
    echo "Run this command to edit:"
    echo "   nano .env"
    echo ""
    read -p "Press Enter after you've configured .env, or Ctrl+C to exit..."
fi

# Validate .env has required variables
echo "🔍 Validating configuration..."
if ! grep -q "LLM_API_KEY=.*[^your-]" .env; then
    echo "❌ LLM_API_KEY is not configured in .env"
    echo "   Please edit .env and add your API key"
    exit 1
fi

echo "✅ Configuration looks good"
echo ""

# Ask user what to do
echo "Select an option:"
echo "  1) Start services (first time / rebuild)"
echo "  2) Start services (quick start)"
echo "  3) Stop services"
echo "  4) View logs"
echo "  5) Restart services"
echo "  6) Status check"
echo ""
read -p "Enter choice [1-6]: " choice

case $choice in
    1)
        echo "🏗️  Building and starting services..."
        docker-compose up -d --build
        ;;
    2)
        echo "▶️  Starting services..."
        docker-compose up -d
        ;;
    3)
        echo "🛑 Stopping services..."
        docker-compose down
        echo "✅ Services stopped"
        exit 0
        ;;
    4)
        echo "📋 Showing logs (Ctrl+C to exit)..."
        docker-compose logs -f
        exit 0
        ;;
    5)
        echo "🔄 Restarting services..."
        docker-compose restart
        ;;
    6)
        echo "📊 Service status:"
        docker-compose ps
        echo ""
        echo "🏥 Health checks:"
        echo "   Backend:  $(curl -s http://localhost:8000/api/health 2>&1 | head -1)"
        echo "   Frontend: $(curl -s -o /dev/null -w '%{http_code}' http://localhost:3000 2>&1)"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "⏳ Waiting for services to start..."
sleep 5

echo ""
echo "🏥 Checking service health..."
for i in {1..30}; do
    if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
        echo "✅ Backend is healthy"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "⚠️  Backend is taking longer than expected to start"
        echo "   Check logs with: docker-compose logs backend"
    fi
    sleep 2
done

for i in {1..30}; do
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo "✅ Frontend is healthy"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "⚠️  Frontend is taking longer than expected to start"
        echo "   Check logs with: docker-compose logs frontend"
    fi
    sleep 2
done

echo ""
echo "✅ AWIES is running!"
echo ""
echo "📱 Access the application:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "📋 Useful commands:"
echo "   View logs:     docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart:       docker-compose restart"
echo ""
