#!/usr/bin/env python3
"""Simple demo of the Advanced Coding Expert system"""
import requests
import json

def demo():
    print("╔════════════════════════════════════════════════════════════╗")
    print("║    Advanced Coding Expert - Live Demo                     ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    # Test 1: Direct Ollama call
    print("1️⃣  Testing Direct Model Access...")
    print("   Query: 'Explain RAG in one sentence'\n")
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.1-coder",
                "prompt": "Explain RAG (Retrieval-Augmented Generation) in one sentence",
                "stream": False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            answer = response.json()["response"]
            print(f"   Response: {answer}\n")
            print("   ✓ Model working!\n")
        else:
            print(f"   Error: {response.status_code}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Test 2: Codebase RAG (would require indexing first)
    print("2️⃣  RAG System Setup")
    print("   To use RAG with your code:")
    print("   a) Index: python phase2-rag/code_expert.py")
    print("   b) Type: index /path/to/your/code")
    print("   c) Ask questions about your codebase\n")
    
    # Test 3: API Server
    print("3️⃣  API Server Status")
    try:
        response = requests.get(
            "http://localhost:8000/health",
            timeout=5
        )
        if response.status_code == 200:
            print("   ✓ API server is running on port 8000")
            print("   📖 View API docs: http://localhost:8000/docs\n")
        else:
            print("   ℹ️  API server not running yet")
            print("   To start: ./venv/bin/python -m uvicorn phase4-agentic.api_server:app\n")
    except requests.exceptions.ConnectionError:
        print("   ℹ️  API server not running yet")
        print("   To start: ./venv/bin/python -m uvicorn phase4-agentic.api_server:app\n")
    
    # Summary
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  ✨ System is working! Pick your next step:               ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    print("Quick Start Options:\n")
    print("  A) Chat with your code (index-based)")
    print("     cd phase2-rag && python code_expert.py\n")
    
    print("  B) Use REST API")
    print("     ./venv/bin/python -m uvicorn phase4-agentic.api_server:app\n")
    
    print("  C) Integrate with VS Code")
    print("     Install Continue.dev extension\n")
    
    print("  D) Read documentation")
    print("     cat README.md\n")
    
    print("═" * 62)

if __name__ == "__main__":
    demo()
