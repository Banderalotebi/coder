#!/usr/bin/env python3
"""
Phase 2: RAG Interactive Demo
Index your codebase and ask the expert questions grounded in your actual code
"""

import sys
from pathlib import Path
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add phase2-rag to path
sys.path.insert(0, str(Path(__file__).parent / "phase2-rag"))

from rag_pipeline import AdvancedCodeRAG
from langchain_community.embeddings import OllamaEmbeddings

OLLAMA_URL = "http://localhost:11434"
EXPERT_MODEL = "expert-llama"

def print_header(text):
    print(f"\n{'='*80}")
    print(f"  {text}")
    print(f"{'='*80}\n")

def check_models():
    """Check if required models are available"""
    try:
        resp = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if resp.status_code != 200:
            return False, []
        
        data = resp.json()
        models = {m['name'].split(':')[0] for m in data.get('models', [])}
        
        needs = []
        if 'nomic-embed-text' not in models:
            needs.append("nomic-embed-text (embedding)")
        if 'expert-llama' not in models:
            needs.append("expert-llama (generation)")
        
        return len(needs) == 0, needs
    except:
        return False, []

def query_with_rag(rag, question):
    """Query using RAG context + expert-llama"""
    try:
        # Search for relevant code
        results = rag.search(question, k=5)
        
        if not results:
            context = "No similar code found in the indexed codebase."
        else:
            context = "\n\n---\n\n".join([
                f"📄 {r['metadata'].get('source', 'unknown')}\n"
                f"Type: {r['metadata'].get('type', 'code')}\n\n"
                f"{r['content'][:800]}"
                for r in results[:3]
            ])
        
        # Build prompt with context
        prompt = f"""You are an expert code analyst. Based on the codebase context provided, answer this question comprehensively:

Question: {question}

Relevant Code Context:
{context}

Provide detailed analysis with specific references to the code shown above."""
        
        # Query expert-llama
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": EXPERT_MODEL,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7
            },
            timeout=120
        )
        
        if response.status_code == 200:
            return response.json().get("response", "No response")
        else:
            return f"Error: HTTP {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

def demo_mode():
    """Run demo with a sample project"""
    print_header("PHASE 2 DEMO: RAG with Sample Code")
    
    print("""This demo indexes the advanced-coding-expert project itself,
then asks the expert questions about it.

This shows how RAG works:
1. Your code is split into semantic chunks
2. Chunks are converted to vectors (embeddings)
3. Questions are also converted to vectors
4. Similar chunks are retrieved
5. Expert-llama analyzes with code context
""")
    
    # Check models
    ready, needs = check_models()
    if not ready:
        print(f"❌ Missing models: {', '.join(needs)}")
        return
    
    print("✅ All models available\n")
    
    # Index a smaller directory
    index_path = Path(__file__).parent / "phase2-rag"
    
    print(f"📚 Indexing: {index_path}")
    print("   (This may take 30-60 seconds on first run)\n")
    
    try:
        rag = AdvancedCodeRAG()
        rag.index_directory(str(index_path))
        print("✅ Indexing complete!\n")
    except Exception as e:
        print(f"❌ Indexing failed: {str(e)}")
        print("\n💡 Tip: If you see embedding errors, ensure:")
        print("   • Ollama is running: ollama serve")
        print("   • Embedding model is installed: ollama pull nomic-embed-text")
        return
    
    # Ask questions
    questions = [
        "What is the main purpose of the AdvancedCodeRAG class?",
        "How does the semantic code splitting work?",
        "What vector database is used and why?",
    ]
    
    print_header("QUERYING WITH RAG CONTEXT")
    
    for i, q in enumerate(questions, 1):
        print(f"\n[Question {i}/{len(questions)}]")
        print(f"❓ {q}\n")
        print("🤖 Expert-llama analyzing your code...\n")
        
        answer = query_with_rag(rag, q)
        
        # Show response
        if len(answer) > 1200:
            print(answer[:1200] + "\n\n[... response continues ...]")
        else:
            print(answer)
        
        print("\n" + "-"*80)

def interactive_mode():
    """Interactive RAG session"""
    print_header("PHASE 2: INTERACTIVE RAG SESSION")
    
    print("""Commands:
  • index <path>  - Index a codebase
  • ask <question> - Ask about indexed code
  • files - Show indexed files
  • exit - Quit
""")
    
    # Check models
    ready, needs = check_models()
    if not ready:
        print(f"❌ Missing models: {', '.join(needs)}")
        print("\nInstall with:")
        for need in needs:
            model = need.split()[0]
            print(f"  ollama pull {model}")
        return
    
    rag = None
    
    while True:
        try:
            cmd = input("\n> ").strip()
            
            if cmd.lower() == 'exit':
                print("Goodbye!")
                break
            
            elif cmd.lower().startswith('index '):
                path = cmd[6:].strip()
                if not Path(path).exists():
                    print(f"❌ Path not found: {path}")
                    continue
                
                print(f"📚 Indexing {path}...")
                try:
                    rag = AdvancedCodeRAG()
                    rag.index_directory(path)
                    print("✅ Indexing complete!")
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
            
            elif cmd.lower().startswith('ask '):
                if not rag:
                    print("❌ No codebase indexed. Use: index <path>")
                    continue
                
                question = cmd[4:].strip()
                print("\n🤖 Analyzing...\n")
                answer = query_with_rag(rag, question)
                print(answer)
            
            elif cmd.lower() == 'files':
                if not rag:
                    print("❌ No codebase indexed.")
                    continue
                print(f"📊 Indexed {len(rag.indexed_files)} files")
            
            else:
                print("❓ Unknown command. Type 'exit' to quit.")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break

def main():
    print_header("PHASE 2: RETRIEVAL AUGMENTED GENERATION")
    
    print("""What RAG does:
    
✅ Chunks your code into semantic pieces
✅ Creates embeddings (vector representations)
✅ Stores chunks in vector database (ChromaDB)
✅ When you ask a question:
   1. Question is embedded
   2. Similar code chunks are found
   3. Expert model uses those chunks as context
   4. Response is grounded in YOUR code

This gives the expert perfect knowledge of your codebase!
    """)
    
    print("\nChoose a mode:")
    print("  1) Demo mode (quick test with sample code)")
    print("  2) Interactive mode (index your own code)")
    print("  3) Skip to next phase")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        demo_mode()
    elif choice == '2':
        interactive_mode()
    elif choice == '3':
        print("\nSkipping to Phase setup...")
        return
    else:
        print("Invalid choice")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
