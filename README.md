# AI App Generator Platform

An AI-powered platform that generates full-stack applications from natural language prompts.

## Architecture

```
┌─────────────────────────────────────────┐
│  Frontend (Next.js 14)                  │
│  - Chat interface                       │
│  - Monaco code editor                   │
│  - Live preview sandbox                 │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  Backend API (Node.js/Fastify)          │
│  - Project management                   │
│  - File operations                      │
│  - WebSocket/SSE streaming              │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  AI Engine (Python/FastAPI)             │
│  - Planner Agent                        │
│  - Architect Agent                      │
│  - Code Generation Agent                │
│  - Validation Agent                     │
└─────────────────────────────────────────┘
```

## Tech Stack

### Frontend
- **Next.js 14** (App Router)
- **TypeScript**
- **Tailwind CSS** + shadcn/ui
- **Monaco Editor** (VS Code engine)
- **Zustand** (state management)
- **TanStack Query** (server state)

### Backend
- **FastAPI** (Python AI agents)
- **Node.js/Fastify** (API layer)
- **PostgreSQL** (primary database)
- **Redis** (cache + queue)
- **Prisma** (ORM)

### AI/ML
- **OpenAI GPT-4o** (planner, frontend generation)
- **Anthropic Claude Sonnet 3.5** (architecture, backend generation)
- **LangChain** (agent orchestration)

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### Installation

```bash
# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Set up database
cd frontend
npx prisma generate
npx prisma db push

# Start development servers
npm run dev
```

The platform will be available at:
- **Frontend**: http://localhost:3000
- **API**: http://localhost:3001
- **AI Engine**: http://localhost:8000

## Project Structure

```
.
├── frontend/              # Next.js application
│   ├── src/
│   │   ├── app/          # App router pages
│   │   ├── components/   # React components
│   │   ├── lib/          # Utilities & helpers
│   │   └── stores/       # Zustand stores
│   └── prisma/           # Database schema
│
├── backend/
│   ├── ai-engine/        # Python AI agents
│   │   ├── agents/       # Agent implementations
│   │   ├── prompts/      # Prompt templates
│   │   └── utils/        # Helper functions
│   │
│   └── api/              # Node.js API layer
│       ├── src/
│       │   ├── routes/   # API endpoints
│       │   ├── services/ # Business logic
│       │   └── utils/    # Helpers
│       └── package.json
│
└── packages/
    └── shared/           # Shared types & utilities
```

## Features

### MVP (Current)
- ✅ Natural language prompt → full Next.js app
- ✅ Multi-agent AI system (Planner, Architect, CodeGen)
- ✅ Real-time code editor with Monaco
- ✅ Live preview in sandboxed iframe
- ✅ File explorer and management
- ✅ Export to ZIP

### Planned
- 🔲 GitHub integration
- 🔲 Real-time collaboration
- 🔲 Deployment to Vercel/Netlify
- 🔲 Component library
- 🔲 Template marketplace

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md)

## License

MIT
