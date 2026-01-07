#!/bin/bash

echo "🚀 AI App Generator - Quick Setup"
echo "=================================="
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+ first."
    exit 1
fi

echo "✅ Node.js version: $(node --version)"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.11+ first."
    exit 1
fi

echo "✅ Python version: $(python3 --version)"

# Check for .env files
echo ""
echo "📝 Checking environment files..."

if [ ! -f ".env" ]; then
    echo "⚠️  No root .env file found. Creating from example..."
    cp .env.example .env
    echo "✅ Created .env - Please add your API keys!"
fi

if [ ! -f "backend/ai-engine/.env" ]; then
    echo "⚠️  No AI engine .env file found. Creating from example..."
    cp backend/ai-engine/.env.example backend/ai-engine/.env
    echo "✅ Created backend/ai-engine/.env - Please add your API keys!"
fi

if [ ! -f "frontend/.env" ]; then
    echo "⚠️  No frontend .env file found. Creating..."
    cat > frontend/.env << 'EOF'
DATABASE_URL="postgresql://postgres:password@localhost:5432/ai_app_generator"
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="dev-secret-change-in-production"
NEXT_PUBLIC_API_URL="http://localhost:3001"
NEXT_PUBLIC_AI_ENGINE_URL="http://localhost:8000"
EOF
    echo "✅ Created frontend/.env"
fi

echo ""
echo "📦 Installing dependencies..."
echo ""

# Install root dependencies
echo "Installing root dependencies..."
npm install

# Install frontend dependencies
echo ""
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Setup Python environment
echo ""
echo "Setting up Python environment..."
cd backend/ai-engine

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Installing Python packages..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null
pip install -q -r requirements.txt
deactivate 2>/dev/null
cd ../..

echo ""
echo "✅ Setup complete!"
echo ""
echo "=================================="
echo "📋 NEXT STEPS:"
echo "=================================="
echo ""
echo "1. Add your API keys to these files:"
echo "   • backend/ai-engine/.env"
echo "     - OPENAI_API_KEY=sk-..."
echo "     - ANTHROPIC_API_KEY=sk-ant-..."
echo ""
echo "2. Start the database:"
echo "   docker-compose up -d"
echo ""
echo "3. Setup the database schema:"
echo "   cd frontend && npx prisma db push && cd .."
echo ""
echo "4. Start the application:"
echo "   npm run dev"
echo ""
echo "Then open: http://localhost:3000"
echo ""
echo "=================================="
