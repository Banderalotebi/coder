#!/usr/bin/env python3
"""
Demo: Phase 2 - RAG (Retrieval Augmented Generation)
Demonstrates semantic code search and expert Q&A powered by Llama 3.1
"""

import sys
from pathlib import Path

# Add phase2-rag to path
sys.path.insert(0, str(Path(__file__).parent / "phase2-rag"))

from rag_pipeline import AdvancedCodeRAG
import requests
import json

OLLAMA_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama3.1-coder"

def print_section(title):
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def check_ollama():
    """Check if Ollama is running"""
    try:
        resp = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        return resp.status_code == 200
    except:
        return False

def query_rag(rag, question, model=DEFAULT_MODEL):
    """Query RAG + LLM"""
    try:
        # Get context from RAG
        results = rag.search(question, k=3)
        
        if not results:
            context = "No similar code found in the indexed codebase."
        else:
            context = "\n---\n".join([
                f"File: {r['metadata'].get('source', 'unknown')}\n"
                f"Type: {r['metadata'].get('type', 'code')}\n"
                f"Content:\n{r['content'][:500]}"
                for r in results[:3]
            ])
        
        # Build prompt
        prompt = f"""You are an expert code analyst. Based on the provided code context and your knowledge, answer this question:

Question: {question}

Code Context:
{context}

Provide a detailed, helpful answer with code examples if relevant."""
        
        # Query Ollama
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7
            },
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json().get("response", "No response")
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print_section("PHASE 2: RAG (Retrieval Augmented Generation) DEMO")
    
    # Check Ollama
    print("📡 Checking Ollama connection...")
    if not check_ollama():
        print("❌ Ollama not running. Start it with: ollama serve")
        return
    print("✅ Ollama is running")
    
    # Initialize RAG
    print("\n🔍 Initializing RAG pipeline...")
    rag = AdvancedCodeRAG()
    
    # Index only the project source files (not venv)
    index_path = Path(__file__).parent / "phase2-rag"
    print(f"\n📚 Indexing codebase: {index_path}")
    print("   (This indexes .py files in phase2-rag)")
    
    try:
        rag.index_directory(str(index_path))
        print("✅ RAG pipeline ready!")
    except Exception as e:
        print(f"⚠️  Note: Embedding model needs to be available in Ollama")
        print(f"   Error: {str(e)}")
        print(f"\n   To fix this, in another terminal run:")
        print(f"   ollama pull nomic-embed-text")
        print(f"\n   For now, showing what RAG does without indexing...")
        return
    
    # Demo questions
    questions = [
        "How is the RAG pipeline implemented?",
        "What are the main components of this system?",
        "Explain semantic code search",
    ]
    
    print_section("DEMO QUERIES")
    for i, question in enumerate(questions, 1):
        print(f"\n[Query {i}] {question}")
        print(f"🤖 {DEFAULT_MODEL} is thinking...\n")
        
        answer = query_rag(rag, question)
        
        # Print answer
        if len(answer) > 1000:
            print(answer[:1000] + "\n\n[... response truncated ...]")
        else:
            print(answer)
        print("\n" + "-"*80)
    
    # Show how to use interactively
    print_section("INTERACTIVE MODE")
    print("""To use the RAG system interactively:

    cd /Users/bander/coder/advanced-coding-expert/phase2-rag
    python code_expert.py

Then you can:
  - Type a question to ask the expert
  - Type 'index' to index a different codebase
  - Type 'exit' to quit

The system will:
  1. Search your indexed code for relevant snippets
  2. Use Llama 3.1 to generate expert-level answers
  3. Ground responses in your actual codebase
""")

if __name__ == "__main__":
    main()
