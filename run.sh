#!/bin/bash

echo "🚀 Starting AI App Generator"
echo "============================="
echo ""

# Check if API keys are configured
if ! grep -q "sk-" backend/ai-engine/.env 2>/dev/null; then
    echo "⚠️  WARNING: No API keys found in backend/ai-engine/.env"
    echo ""
    echo "Please add your API keys:"
    echo "  OPENAI_API_KEY=sk-your-key-here"
    echo "  ANTHROPIC_API_KEY=sk-ant-your-key-here"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if PostgreSQL is running
if ! nc -z localhost 5432 2>/dev/null; then
    echo "⚠️  PostgreSQL not detected on port 5432"
    echo "Starting with docker-compose..."
    docker-compose up -d
    echo "Waiting for database to be ready..."
    sleep 3
fi

echo "✅ Database ready"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down..."
    kill $FRONTEND_PID 2>/dev/null
    kill $BACKEND_PID 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

# Start AI Engine
echo "🤖 Starting AI Engine (Python FastAPI)..."
cd backend/ai-engine
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null
python main.py &
BACKEND_PID=$!
cd ../..

# Wait a moment for backend to start
sleep 2

# Start Frontend
echo "🎨 Starting Frontend (Next.js)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "=================================="
echo "✅ SERVERS RUNNING"
echo "=================================="
echo ""
echo "Frontend:  http://localhost:3000"
echo "AI Engine: http://localhost:8000"
echo "API Docs:  http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"
echo "=================================="
echo ""

# Wait for both processes
wait
