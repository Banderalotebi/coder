#!/usr/bin/env python3
"""System verification script"""
import requests
import sys
import importlib.util

def test_system():
    """Test all components"""
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   Advanced Coding Expert - System Verification             ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    # Test Ollama
    print("🔍 Testing Ollama Connection...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        models = response.json()["models"]
        print(f"✓ Ollama Connected!")
        print(f"  Found {len(models)} models:")
        for model in models[:2]:
            name = model['name']
            size = f"{model['size'] / 1e9:.1f}GB"
            print(f"    - {name} ({size})")
        print()
    except Exception as e:
        print(f"✗ Ollama Error: {e}\n")
        return False
    
    # Test Python imports (load from files directly)
    print("📦 Testing Python Modules...")
    try:
        # Load RAG pipeline directly from file
        spec = importlib.util.spec_from_file_location(
            "rag_pipeline",
            "phase2-rag/rag_pipeline.py"
        )
        rag_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(rag_mod)
        print("✓ RAG Pipeline module loads")
    except Exception as e:
        print(f"✗ RAG Pipeline: {e}")
        return False
    
    try:
        # Load Agentic Tools directly
        spec = importlib.util.spec_from_file_location(
            "agentic_tools",
            "phase4-agentic/agentic_tools.py"
        )
        agent_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(agent_mod)
        print("✓ Agentic Tools module loads")
    except Exception as e:
        print(f"✗ Agentic Tools: {e}")
        return False
    
    print()
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   ✨ System Ready to Use!                                 ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    print("🚀 Quick Start Commands:\n")
    print("  1. Interactive RAG Chat:")
    print("     cd phase2-rag && python code_expert.py\n")
    print("  2. Start API Server (from root):")
    print("     python -m uvicorn phase4-agentic.api_server:app --port 8000\n")
    print("         (or: ./venv/bin/python phase4-agentic/api_server.py)\n")
    print("  3. Test a model:")
    print("     python -c \"import ollama; print(ollama.generate('llama3.1', 'Hello!'))\"")
    print("\n📖 Read README.md for complete guide\n")
    
    return True

if __name__ == "__main__":
    success = test_system()
    sys.exit(0 if success else 1)
