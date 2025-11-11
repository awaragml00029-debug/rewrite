#!/bin/bash

# AWIES Frontend Start Script

echo "================================"
echo "Starting AWIES Frontend"
echo "================================"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
else
    echo "✅ Dependencies already installed"
fi

# Start development server
echo ""
echo "🚀 Starting development server..."
echo "📖 Frontend: http://localhost:3000"
echo "🔌 API Proxy: http://localhost:3000/api -> http://localhost:8000/api"
echo ""
echo "💡 Make sure the backend server is running on port 8000!"
echo ""

npm run dev
