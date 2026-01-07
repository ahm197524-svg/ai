# Setup Guide - AI App Generator Platform

Complete setup guide for local development.

## Prerequisites

- **Node.js** 18+ and npm 9+
- **Python** 3.11+
- **PostgreSQL** 15+
- **Redis** 7+
- **OpenAI API Key**
- **Anthropic API Key**

## Step 1: Clone and Install Dependencies

```bash
# Clone the repository
git clone <your-repo-url>
cd ai-app-generator

# Install root dependencies
npm install

# Install frontend dependencies
cd frontend
npm install

# Install Python dependencies
cd ../backend/ai-engine
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2: Environment Variables

### Frontend (.env)

Create `frontend/.env`:

```env
# Database
DATABASE_URL="postgresql://postgres:password@localhost:5432/ai_app_generator"

# NextAuth
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="your-secret-key-generate-with-openssl-rand-base64-32"

# Backend URLs
NEXT_PUBLIC_API_URL="http://localhost:3001"
NEXT_PUBLIC_AI_ENGINE_URL="http://localhost:8000"
```

### AI Engine (.env)

Create `backend/ai-engine/.env`:

```env
# AI API Keys
OPENAI_API_KEY="sk-..."
ANTHROPIC_API_KEY="sk-ant-..."

# Database & Cache
DATABASE_URL="postgresql://postgres:password@localhost:5432/ai_app_generator"
REDIS_URL="redis://localhost:6379"

# Server
HOST="0.0.0.0"
PORT=8000
ENVIRONMENT="development"
```

## Step 3: Database Setup

```bash
# Start PostgreSQL (if using Docker)
docker run --name postgres-ai \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=ai_app_generator \
  -p 5432:5432 \
  -d postgres:15

# Start Redis (if using Docker)
docker run --name redis-ai \
  -p 6379:6379 \
  -d redis:7

# Run Prisma migrations
cd frontend
npx prisma generate
npx prisma db push
```

## Step 4: Start Development Servers

### Option A: All at once (Recommended)

```bash
# From project root
npm run dev
```

This starts:
- Frontend: http://localhost:3000
- AI Engine: http://localhost:8000

### Option B: Individual servers

**Terminal 1 - Frontend:**
```bash
cd frontend
npm run dev
```

**Terminal 2 - AI Engine:**
```bash
cd backend/ai-engine
source venv/bin/activate
python main.py
```

## Step 5: Verify Installation

1. **Frontend**: Open http://localhost:3000
   - Should see the landing page

2. **AI Engine**: Open http://localhost:8000/docs
   - Should see FastAPI Swagger UI

3. **Test Generation**:
   - Create a new project
   - Try prompt: "Build a simple landing page"
   - Watch the AI generate code in real-time

## Common Issues

### Database Connection Error

```
Error: Can't reach database server at localhost:5432
```

**Solution**: Ensure PostgreSQL is running
```bash
# Check if running
docker ps | grep postgres

# Start if not running
docker start postgres-ai
```

### Redis Connection Error

```
Error: Error 61 connecting to localhost:6379
```

**Solution**: Start Redis
```bash
docker start redis-ai
```

### AI API Key Error

```
Error: Invalid API key provided
```

**Solution**: Verify your API keys are correct in `.env` files
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/settings/keys

### Port Already in Use

```
Error: Port 3000 is already in use
```

**Solution**: Kill the process or use different port
```bash
# Find process
lsof -i :3000

# Kill process
kill -9 <PID>
```

## Next Steps

- Read [ARCHITECTURE.md](./ARCHITECTURE.md) for system overview
- See [API.md](./API.md) for API documentation
- Check [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment

## Development Tips

### Hot Reload

Both frontend and backend support hot reload:
- Frontend: Changes to `.tsx` files auto-reload
- Backend: Changes to `.py` files auto-reload (uvicorn --reload)

### Database Changes

After modifying `prisma/schema.prisma`:
```bash
npx prisma generate
npx prisma db push
```

### Debugging

**Frontend:**
- Use React DevTools browser extension
- Check Next.js dev console in terminal

**Backend:**
- Check FastAPI logs in terminal
- Use `/docs` endpoint for API testing

### Testing Prompts

Good test prompts for development:
1. "Build a landing page with hero and features"
2. "Create a todo app with CRUD operations"
3. "Build a blog with markdown support"
4. "Make a dashboard with charts"

## Support

Having issues? Check:
- GitHub Issues
- Discord Community
- Documentation site
