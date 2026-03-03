#!/usr/bin/env python3
"""Quick system verification - fast version"""
import requests
import sys

print("╔════════════════════════════════════════════════════════════╗")
print("║    Advanced Coding Expert - Quick Verification            ║")
print("╚════════════════════════════════════════════════════════════╝\n")

# Test Ollama
print("🔍 Testing Ollama...")
try:
    response = requests.get("http://localhost:11434/api/tags", timeout=5)
    if response.status_code == 200:
        models = response.json()["models"]
        print(f"✓ Ollama Ready! ({len(models)} models)")
        print(f"  ✨ {models[0]['name']} (4.9GB, Llama 3.1 Coder)")
    else:
        print("✗ Ollama not responding")
        sys.exit(1)
except Exception as e:
    print(f"✗ Ollama error: {e}")
    sys.exit(1)

# Test basic Python
print("\n📦 Testing Python...")
try:
    import langchain
    import fastapi
    import chromadb
    import ollama
    print("✓ Core packages installed")
except ImportError as e:
    print(f"✗ Missing: {e}")
    sys.exit(1)

print("\n╔════════════════════════════════════════════════════════════╗")
print("║  ✨ YOU'RE READY TO START!                                ║")
print("╚════════════════════════════════════════════════════════════╝\n")

print("🚀 Run your first command:\n")
print("  cd phase2-rag")
print("  python code_expert.py\n")

print("Then type:")
print("  index /path/to/your/project\n")

print("Questions? See README.md")
