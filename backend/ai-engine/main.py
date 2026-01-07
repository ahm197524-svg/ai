from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import asyncio
import json

from agents.planner import PlannerAgent
from agents.architect import ArchitectAgent
from agents.codegen import CodeGenAgent
from config import settings

app = FastAPI(
    title="AI App Generator Engine",
    description="AI agents for generating full-stack applications",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
planner = PlannerAgent()
architect = ArchitectAgent()
codegen = CodeGenAgent()


# ============================================================================
# MODELS
# ============================================================================

class GenerateRequest(BaseModel):
    prompt: str
    project_id: str
    conversation_id: Optional[str] = None
    framework: str = "nextjs"
    language: str = "typescript"
    styling: str = "tailwind"


class GenerateResponse(BaseModel):
    generation_id: str
    status: str
    message: str


class GenerationEvent(BaseModel):
    type: str
    data: Dict[str, Any]


# ============================================================================
# ROUTES
# ============================================================================

@app.get("/")
async def root():
    return {
        "name": "AI App Generator Engine",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/generate", response_model=GenerateResponse)
async def generate_app(request: GenerateRequest):
    """
    Initiate app generation from a prompt.
    Returns a generation_id that can be used to stream progress.
    """
    generation_id = f"gen_{request.project_id}_{asyncio.get_event_loop().time()}"

    # In production, this would be queued to a task queue (Celery/Redis)
    # For MVP, we'll process it in the background
    asyncio.create_task(run_generation(generation_id, request))

    return GenerateResponse(
        generation_id=generation_id,
        status="started",
        message="Generation started. Use /generate/{generation_id}/stream to watch progress."
    )


@app.get("/generate/{generation_id}/stream")
async def stream_generation(generation_id: str):
    """
    Server-Sent Events endpoint to stream generation progress.
    """
    async def event_generator():
        # In production, this would read from Redis pub/sub
        # For MVP, we'll simulate the streaming

        yield f"data: {json.dumps({'type': 'started', 'message': 'Generation started'})}\n\n"

        await asyncio.sleep(1)
        yield f"data: {json.dumps({'type': 'planning', 'message': 'Planning application architecture...'})}\n\n"

        await asyncio.sleep(2)
        yield f"data: {json.dumps({'type': 'architecting', 'message': 'Designing file structure...'})}\n\n"

        await asyncio.sleep(2)
        yield f"data: {json.dumps({'type': 'generating', 'message': 'Generating code files...'})}\n\n"

        await asyncio.sleep(3)
        yield f"data: {json.dumps({'type': 'completed', 'message': 'Generation complete!'})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )


# ============================================================================
# GENERATION PIPELINE
# ============================================================================

async def run_generation(generation_id: str, request: GenerateRequest):
    """
    Main generation pipeline that orchestrates all agents.

    Steps:
    1. Planner Agent - Parse prompt and extract requirements
    2. Architect Agent - Design system architecture
    3. CodeGen Agent - Generate actual code files
    4. Validation Agent - Validate generated code
    """
    try:
        # Step 1: Planning
        print(f"[{generation_id}] Step 1: Planning...")
        plan = await planner.create_plan(request.prompt)
        print(f"[{generation_id}] Plan created: {plan}")

        # Step 2: Architecture
        print(f"[{generation_id}] Step 2: Designing architecture...")
        architecture = await architect.design_architecture(
            plan=plan,
            framework=request.framework,
            language=request.language,
            styling=request.styling
        )
        print(f"[{generation_id}] Architecture designed")

        # Step 3: Code Generation
        print(f"[{generation_id}] Step 3: Generating code...")
        files = await codegen.generate_files(
            plan=plan,
            architecture=architecture
        )
        print(f"[{generation_id}] Generated {len(files)} files")

        # Step 4: Save to database
        # TODO: Save files to database

        print(f"[{generation_id}] ✅ Generation complete!")

    except Exception as e:
        print(f"[{generation_id}] ❌ Error: {str(e)}")
        raise


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development"
    )
