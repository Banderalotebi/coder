"""
FastAPI Server for the Advanced Coding Expert system
Simple version that works without complex imports
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Advanced Coding Expert API",
    description="Llama 3.1 + RAG + Agentic Workflows",
    version="1.0.0"
)

OLLAMA_URL = "http://localhost:11434"
# expert-llama is configured with unlimited output tokens and 32k context
DEFAULT_MODEL = "expert-llama"


# ==================== Data Models ====================

class QueryRequest(BaseModel):
    """Query the model"""
    question: str = Field(..., description="Your question")
    temperature: float = Field(0.7, ge=0.0, le=1.0)


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    models_available: List[str]


# ==================== Endpoints ====================

@app.get("/")
async def root():
    """API documentation"""
    return {
        "title": "Advanced Coding Expert API",
        "version": "1.0.0",
        "endpoints": {
            "health": "GET /health",
            "query": "POST /query",
            "models": "GET /models"
        },
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check system health"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [m["name"] for m in models]
            return {
                "status": "healthy",
                "models_available": model_names
            }
    except:
        pass
    
    return {
        "status": "degraded",
        "models_available": []
    }


@app.get("/models")
async def list_models():
    """List available models"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return {
                "status": "success",
                "models": [
                    {
                        "name": m["name"],
                        "size_gb": round(m["size"] / 1e9, 1)
                    }
                    for m in models
                ]
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/query")
async def query_model(request: QueryRequest):
    """Query the model directly"""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": DEFAULT_MODEL,
                "prompt": request.question,
                "temperature": request.temperature,
                "stream": False
            },
            timeout=60
        )
        
        if response.status_code == 200:
            answer = response.json().get("response", "")
            return {
                "status": "success",
                "question": request.question,
                "answer": answer
            }
        else:
            return {
                "status": "error",
                "message": "Model query failed"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@app.post("/ask")
async def ask_question(question: str, temperature: float = 0.7):
    """Simple query endpoint (query string parameter)"""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": DEFAULT_MODEL,
                "prompt": question,
                "temperature": temperature,
                "stream": False
            },
            timeout=60
        )
        
        if response.status_code == 200:
            return {
                "question": question,
                "answer": response.json().get("response", "")
            }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
