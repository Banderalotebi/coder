"""

from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import logging
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from phase2_rag.code_expert import OllamaCodeExpert
from phase4_agentic.agentic_tools import CodeAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Advanced Coding Expert API",
    description="TechPartner AI Coder - Llama 3.1 + RAG + Agentic Workflows",
    version="1.0.0"
)

# Security: Admin secret from environment
ADMIN_SECRET = os.getenv("ADMIN_SECRET", "Admin@6565")


# ==================== Security Dependency ====================

def verify_admin(authorization: str = Header(None), x_admin_token: str = Header(None)):
    """Verify admin access using Bearer token or custom header"""
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
    elif x_admin_token:
        token = x_admin_token
        
    if token != ADMIN_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized TechPartner Access")
    return True


# ==================== Data Models ====================

class QueryRequest(BaseModel):
    """RAG-powered code question"""
    question: str = Field(..., description="Your question about the codebase")
    use_rag: bool = Field(True, description="Use RAG context")
    temperature: float = Field(0.7, ge=0.0, le=1.0)


class TaskRequest(BaseModel):
    """Agentic task request"""
    task: str = Field(..., description="Coding task to complete")
    use_tools: bool = Field(True, description="Allow tool usage")
    max_iterations: int = Field(5, ge=1, le=20)


class IndexRequest(BaseModel):
    """Index a directory for RAG"""
    directory: str = Field(..., description="Directory path to index")
    file_patterns: Optional[List[str]] = Field(
        None,
        description="File patterns to include (e.g., ['.py', '.ts'])"
    )


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    models_available: List[str]
    features: List[str]


# ==================== Initialize Systems ====================

try:
    expert = OllamaCodeExpert()
    agent = CodeAgent()
    logger.info("✓ Systems initialized successfully")
except Exception as e:
    logger.error(f"Initialization error: {e}")
    expert = None
    agent = None


# ==================== Endpoints ====================

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if expert and agent else "degraded",
        "models_available": ["llama2:7b", "llama2:13b"],
        "features": ["RAG", "Agentic", "Fine-tuning"]
    }


@app.post("/query")
async def query_codebase(request: QueryRequest, admin: bool = Depends(verify_admin)) -> dict:
    """
    Query your codebase with RAG-powered Llama.
    
    Example:
    ```json
    {
      "question": "How is authentication implemented in this project?",
      "use_rag": true
    }
    ```
    """
    if not expert:
        raise HTTPException(status_code=503, detail="Expert system not initialized")
    
    try:
        answer = expert.query(
            request.question,
            use_rag=request.use_rag,
            temperature=request.temperature
        )
        return {
            "question": request.question,
            "answer": answer,
            "rag_enabled": request.use_rag
        }
    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/task")
async def complete_task(request: TaskRequest, admin: bool = Depends(verify_admin)) -> dict:
    """
    Complete a coding task using agentic workflows.
    
    The agent will:
    1. Search your codebase
    2. Analyze the code structure
    3. Check syntax and run linters
    4. Execute code to test solutions
    5. Provide fixed/optimized code
    
    Example:
    ```json
    {
      "task": "Fix the database connection leak and optimize the query",
      "use_tools": true
    }
    ```
    """
    if not agent:
        raise HTTPException(status_code=503, detail="Agent system not initialized")
    
    try:
        solution = agent.process_task(request.task)
        return {
            "task": request.task,
            "solution": solution,
            "tools_used": request.use_tools
        }
    except Exception as e:
        logger.error(f"Task error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/index")
async def index_codebase(request: IndexRequest, admin: bool = Depends(verify_admin)) -> dict:
    """
    Index a directory for RAG semantic search.
    
    This will:
    1. Scan all code files recursively
    2. Split by semantic chunks (functions/classes)
    3. Create embeddings with local model
    4. Store in ChromaDB vector store
    
    Example:
    ```json
    {
      "directory": "/path/to/project",
      "file_patterns": [".py", ".ts", ".js"]
    }
    ```
    """
    if not expert:
        raise HTTPException(status_code=503, detail="Expert system not initialized")
    
    try:
        patterns = request.file_patterns or [".py", ".ts", ".js"]
        expert.rag.index_directory(request.directory, patterns)
        return {
            "status": "success",
            "directory": request.directory,
            "patterns": patterns,
            "message": "Indexing complete. RAG is ready."
        }
    except Exception as e:
        logger.error(f"Indexing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search")
async def search_codebase(q: str, k: int = 5) -> dict:
    """
    Direct semantic search across codebase.
    
    Query parameters:
    - q: Search query
    - k: Number of results (default: 5)
    """
    if not expert:
        raise HTTPException(status_code=503, detail="Expert system not initialized")
    
    try:
        results = expert.rag.search(q, k=k)
        return {
            "query": q,
            "num_results": len(results),
            "results": results
        }
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tools")
async def list_tools() -> dict:
    """List available agentic tools"""
    return {
        "tools": [
            {
                "name": "linter",
                "description": "Check code for errors and style issues",
                "methods": ["check_syntax", "run_pylint", "run_eslint"]
            },
            {
                "name": "search",
                "description": "Search codebase for patterns and definitions",
                "methods": ["grep_search", "find_function"]
            },
            {
                "name": "executor",
                "description": "Execute and test code safely",
                "methods": ["execute_python", "execute_with_input"]
            },
            {
                "name": "navigator",
                "description": "Navigate and read files",
                "methods": ["read_file", "list_directory", "analyze_structure"]
            },
            {
                "name": "techpartner",
                "description": "Query TechPartner CRM and system (requires admin)",
                "methods": ["get_health", "get_crm_stats", "get_leads", "get_companies"]
            }
        ]
    }


# ==================== Documentation ====================

@app.get("/")
async def root():
    """API documentation"""
    return {
        "title": "Advanced Coding Expert API",
        "version": "1.0.0",
        "endpoints": {
            "health": "GET /health - System status",
            "query": "POST /query - Ask about your codebase",
            "task": "POST /task - Complete a coding task",
            "index": "POST /index - Index codebase for RAG",
            "search": "GET /search?q=... - Direct semantic search",
            "tools": "GET /tools - List available tools"
        },
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
