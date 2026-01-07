# System Architecture

Complete technical architecture of the AI App Generator platform.

## Overview

The platform uses a multi-agent AI system to generate full-stack applications from natural language prompts.

```
User Prompt → Planner → Architect → CodeGen → Validation → Preview
```

## Components

### 1. Frontend (Next.js)

**Location**: `/frontend`

**Tech Stack**:
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS + shadcn/ui
- Monaco Editor
- TanStack Query
- Zustand

**Key Features**:
- Real-time chat interface with AI
- Monaco code editor with syntax highlighting
- Live preview in sandboxed iframe
- File tree navigation
- Project management dashboard

**File Structure**:
```
frontend/
├── src/
│   ├── app/                 # Next.js app router
│   │   ├── page.tsx        # Landing page
│   │   ├── projects/       # Projects routes
│   │   └── api/            # API routes (future)
│   ├── components/
│   │   ├── ui/             # shadcn/ui components
│   │   ├── chat/           # Chat interface
│   │   ├── editor/         # Code editor
│   │   ├── preview/        # Live preview
│   │   └── project/        # File tree, etc.
│   ├── lib/                # Utilities
│   ├── stores/             # Zustand stores
│   └── types/              # TypeScript types
└── prisma/
    └── schema.prisma       # Database schema
```

### 2. AI Engine (Python/FastAPI)

**Location**: `/backend/ai-engine`

**Tech Stack**:
- FastAPI
- OpenAI GPT-4o
- Anthropic Claude Sonnet 3.5
- LangChain (future)
- Redis (for task queue)

**Agents**:

#### Planner Agent
- **Model**: GPT-4o
- **Role**: Parse prompts, extract requirements
- **Input**: Natural language prompt
- **Output**: Structured plan with features, pages, entities

#### Architect Agent
- **Model**: Claude Sonnet 3.5
- **Role**: Design system architecture
- **Input**: Plan from Planner
- **Output**: File structure, database schema, API routes, dependencies

#### CodeGen Agent
- **Model**: GPT-4o (frontend), Claude (backend)
- **Role**: Generate actual code files
- **Input**: Plan + Architecture
- **Output**: Complete code files with proper types, error handling

**File Structure**:
```
backend/ai-engine/
├── agents/
│   ├── planner.py          # Planner agent
│   ├── architect.py        # Architect agent
│   ├── codegen.py          # Code generation
│   └── validator.py        # Validation (future)
├── prompts/                # Prompt templates
├── utils/                  # Helper functions
├── main.py                 # FastAPI app
└── config.py               # Configuration
```

### 3. Database (PostgreSQL)

**Schema Overview**:

```sql
users               # User accounts
projects            # User projects
project_files       # Generated code files
conversations       # Chat conversations
messages            # Chat messages
generations         # Generation jobs
generation_steps    # Individual agent steps
```

See `frontend/prisma/schema.prisma` for complete schema.

### 4. Cache & Queue (Redis)

**Usage**:
- Session storage
- Real-time generation progress
- Task queue (future)
- API response caching

## Data Flow

### 1. Project Creation & Generation

```
User enters prompt in chat
       ↓
Frontend sends to /generate endpoint
       ↓
AI Engine creates generation job
       ↓
Planner Agent analyzes prompt
       ↓
Architect Agent designs structure
       ↓
CodeGen Agent generates files (parallel)
       ↓
Files saved to database
       ↓
Frontend receives updates via SSE
       ↓
Files appear in code editor
       ↓
Preview sandbox starts automatically
```

### 2. File Editing

```
User edits file in Monaco
       ↓
Debounced save (500ms)
       ↓
PUT /api/projects/{id}/files/{path}
       ↓
Update database
       ↓
Trigger preview reload
```

### 3. Iterative Refinement

```
User: "Add a contact form"
       ↓
AI analyzes existing code
       ↓
Generates only new/modified files
       ↓
Preserves user edits
       ↓
Updates preview
```

## API Endpoints

### AI Engine (Port 8000)

```
POST   /generate
GET    /generate/{id}/stream      # SSE for progress
GET    /health
```

### Frontend API Routes (Future)

```
POST   /api/projects
GET    /api/projects/{id}
PUT    /api/projects/{id}/files/{path}
POST   /api/projects/{id}/export
```

## Security

### Sandboxing Strategy

**Current (MVP)**:
- Iframe with `sandbox` attribute
- Limited to `allow-scripts allow-same-origin`

**Future (Production)**:
- Kubernetes pods with resource limits
- Network isolation
- Read-only root filesystem
- Auto-stop after 30 minutes

### API Security

- Rate limiting (100 req/min)
- API key authentication
- CORS restrictions
- Input validation with Zod

## Scaling Strategy

### Phase 1 (MVP): Single Server
- Frontend: Vercel
- Backend: Railway/Render
- Database: Supabase
- Redis: Upstash

### Phase 2 (Growth): Horizontal Scaling
- Frontend: Vercel (auto-scale)
- Backend: Multiple instances behind load balancer
- Database: PostgreSQL with read replicas
- Redis: Redis Cluster

### Phase 3 (Scale): Microservices
- Separate AI engine instances
- Task queue with Celery
- Kubernetes for sandboxes
- CDN for static assets

## Performance Optimizations

### Frontend
- Code splitting (Next.js automatic)
- Image optimization
- Monaco lazy loading
- Virtualized file tree for large projects

### Backend
- Parallel file generation (batches of 5)
- Model selection based on complexity
- Response caching
- Connection pooling

### Cost Optimization
- Use GPT-4o-mini for simple files
- Cache common components
- Semantic search to avoid regeneration
- User tier limits

## Monitoring

**Metrics to Track**:
- Generation success rate
- Average generation time
- AI API costs per generation
- Error rates by agent
- User engagement (prompts per project)

**Tools** (Future):
- Sentry (errors)
- DataDog (metrics)
- LogTail (logs)
- PostHog (analytics)

## Future Enhancements

1. **Multi-model routing**: Route to cheapest model that can handle complexity
2. **Component library**: RAG-based component reuse
3. **Screenshot to code**: Vision models for Figma → code
4. **Real-time collaboration**: WebSocket-based collaborative editing
5. **Deployment automation**: One-click deploy to Vercel/Netlify
6. **Testing generation**: Auto-generate unit/e2e tests
