#!/usr/bin/env python3
"""
Phase 2 Demo: Direct Llama Query (No RAG indexing needed)
Shows the system working end-to-end without embedding setup complexity
"""

import requests
import json
from pathlib import Path

OLLAMA_URL = "http://localhost:11434"
# expert-llama is configured with unlimited output tokens and 32k context
DEFAULT_MODEL = "expert-llama"

def print_section(title):
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def check_ollama():
    """Check if Ollama is running"""
    try:
        resp = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        if resp.status_code == 200:
            data = resp.json()
            models = [m['name'] for m in data.get('models', [])]
            print(f"✅ Ollama running with {len(models)} models")
            if DEFAULT_MODEL in models:
                print(f"   🎯 Using: {DEFAULT_MODEL}")
            return True
        return False
    except:
        return False

def query_llama(question, model=DEFAULT_MODEL):
    """Query Llama 3.1 Coder directly"""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model,
                "prompt": question,
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
    print_section("PHASE 2 DEMO: Advanced Coding Expert with Llama 3.1")
    
    # Check Ollama
    print("📡 Checking Ollama connection...")
    if not check_ollama():
        print("❌ Ollama not running. Start it with: ollama serve")
        return
    
    # Demo questions
    questions = [
        ("What is RAG (Retrieval Augmented Generation)?", 
         "AI/ML Concept"),
        ("How do you optimize a slow database query?", 
         "Database"),
        ("What are the best practices for API design?", 
         "Software Architecture"),
        ("Explain the difference between sync and async code",
         "Programming Concepts"),
    ]
    
    print_section("QUERYING LLAMA 3.1 CODER")
    print("Each question demonstrates the expert's knowledge:\n")
    
    for question, category in questions:
        print(f"\n📌 [{category}]")
        print(f"   Question: {question}")
        print(f"\n🤖 Llama 3.1 Coder response:\n")
        
        answer = query_llama(question)
        
        # Print response (truncate if very long)
        if len(answer) > 600:
            print(answer[:600] + "\n   [... truncated ...]")
        else:
            print(answer)
        
        print(f"\n{'-'*80}")
    
    print_section("NEXT STEPS")
    print("""To use the full RAG system with your codebase:

1. Install embedding model:
   ollama pull nomic-embed-text

2. Run the interactive expert:
   cd /Users/bander/coder/advanced-coding-expert/phase2-rag
   python code_expert.py

3. In the interactive session:
   - Type 'index' to index your codebase
   - Then ask questions about your code
   - The expert will use RAG to provide contextual answers

The RAG system:
  • Indexes your code into vectors
  • Finds similar code snippets for any question
  • Uses those chunks to ground AI responses
  • Provides expert-level answers based on YOUR codebase
""")

if __name__ == "__main__":
    main()
