# Quick Start Guide

Get the AI App Generator running in 10 minutes.

## TL;DR

```bash
# 1. Install dependencies
npm install
cd frontend && npm install
cd ../backend/ai-engine && pip install -r requirements.txt

# 2. Setup environment
cp .env.example .env
# Edit .env with your API keys

# 3. Start database
docker-compose up -d  # or use your local PostgreSQL

# 4. Setup database schema
cd frontend && npx prisma db push

# 5. Start everything
cd ../.. && npm run dev
```

Open http://localhost:3000 🎉

## Detailed Steps

### 1. Get API Keys (5 min)

**OpenAI** (Required for Planner & CodeGen):
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy key (starts with `sk-...`)
4. Add $10+ credits to your account

**Anthropic** (Required for Architect):
1. Go to https://console.anthropic.com/settings/keys
2. Click "Create Key"
3. Copy key (starts with `sk-ant-...`)
4. You get $5 free credits

### 2. Database Setup (2 min)

**Option A: Docker (Easiest)**
```bash
docker-compose up -d
```

**Option B: Local PostgreSQL**
```bash
# Install PostgreSQL 15+
brew install postgresql@15  # macOS
# or apt install postgresql-15  # Ubuntu

# Create database
createdb ai_app_generator
```

### 3. Environment Configuration (1 min)

Create `frontend/.env`:
```env
DATABASE_URL="postgresql://postgres:password@localhost:5432/ai_app_generator"
NEXTAUTH_SECRET="generate-me-with-openssl-rand-base64-32"
NEXTAUTH_URL="http://localhost:3000"
NEXT_PUBLIC_API_URL="http://localhost:3001"
NEXT_PUBLIC_AI_ENGINE_URL="http://localhost:8000"
```

Create `backend/ai-engine/.env`:
```env
OPENAI_API_KEY="sk-your-key"
ANTHROPIC_API_KEY="sk-ant-your-key"
DATABASE_URL="postgresql://postgres:password@localhost:5432/ai_app_generator"
REDIS_URL="redis://localhost:6379"
```

### 4. Install & Run (2 min)

```bash
# Install dependencies
npm install

# Setup database
cd frontend
npx prisma generate
npx prisma db push

# Start all servers
cd ..
npm run dev
```

**Services will start at:**
- Frontend: http://localhost:3000
- AI Engine: http://localhost:8000
- API Docs: http://localhost:8000/docs

## First Generation

1. Open http://localhost:3000
2. Click "Start Building"
3. Enter prompt:
   ```
   Build a landing page with a hero section,
   features grid, and contact form
   ```
4. Watch the AI generate your app!
5. See live preview on the right panel

## Example Prompts to Try

### Simple
```
Build a personal portfolio website with about and projects sections
```

### Medium
```
Create a blog with MDX support, categories, and search functionality
```

### Complex
```
Build a SaaS app with authentication, Stripe payments,
and a user dashboard showing subscription status
```

## What Gets Generated

For each prompt, the AI creates:
- ✅ Complete Next.js project structure
- ✅ All page components with routing
- ✅ UI components (buttons, cards, forms)
- ✅ API routes (if needed)
- ✅ Database schema (if needed)
- ✅ Tailwind styling
- ✅ TypeScript types
- ✅ Configuration files

## Iterative Development

After initial generation, refine your app:
```
User: "Add a dark mode toggle"
AI: *generates theme switcher and updates all components*

User: "Make the contact form send emails"
AI: *adds email API route and form submission logic*
```

## Troubleshooting

### "Cannot connect to database"
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Start if needed
docker-compose up -d
```

### "Invalid API key"
- Verify keys are correctly set in `.env`
- Check you have credits remaining
- Ensure no extra spaces in the key

### "Port 3000 already in use"
```bash
# Kill the process
lsof -i :3000
kill -9 <PID>
```

### Generation fails or produces errors
- Check AI Engine logs in terminal
- Verify API keys have sufficient credits
- Try a simpler prompt first
- Check http://localhost:8000/docs to test API directly

## Next Steps

- 📖 Read [ARCHITECTURE.md](./ARCHITECTURE.md) to understand how it works
- 🚀 See [DEPLOYMENT.md](./DEPLOYMENT.md) to deploy to production
- 🎨 Customize the UI in `frontend/src/components`
- 🤖 Improve agents in `backend/ai-engine/agents`

## Cost Estimation

Approximate AI API costs per generation:

| Complexity | Files | OpenAI | Anthropic | Total |
|------------|-------|--------|-----------|-------|
| Simple     | 10-15 | $0.10  | $0.05     | $0.15 |
| Medium     | 30-40 | $0.30  | $0.15     | $0.45 |
| Complex    | 60+   | $0.60  | $0.30     | $0.90 |

**MVP Budget**: $50-100 for testing/development

## Getting Help

- 📚 Documentation: `/docs`
- 🐛 Issues: GitHub Issues
- 💬 Community: Discord
- 📧 Email: support@example.com
