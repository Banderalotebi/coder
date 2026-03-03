"""
RAG + LLM Integration: Query your codebase with Llama 2
"""

import logging
from typing import Optional
import requests
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from rag_pipeline import AdvancedCodeRAG

logger = logging.getLogger(__name__)


class OllamaCodeExpert:
    """
    Combines RAG with Ollama's Llama 2 for expert code answers.
    """

    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "llama2:7b"):
        self.ollama_url = ollama_url
        self.model = model
        self.rag = AdvancedCodeRAG()

    def query(self, question: str, use_rag: bool = True, temperature: float = 0.7) -> str:
        """
        Ask the code expert a question.
        
        Args:
            question: Your question about the codebase
            use_rag: Whether to augment with RAG context
            temperature: LLM creativity (0.0-1.0)
            
        Returns:
            Expert answer with context
        """
        
        if use_rag:
            rag_output = self.rag.query_with_context(question, k=7)
            prompt = rag_output['prompt']
            context_info = f"\n[Context: {rag_output['num_chunks']} relevant chunks retrieved]"
        else:
            prompt = question
            context_info = ""

        # Call Ollama
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": temperature,
                    "stream": False
                },
                timeout=60
            )
            response.raise_for_status()
            
            answer = response.json().get('response', '')
            
            print(f"\n{'='*80}")
            print(f"QUESTION: {question}")
            print(f"{'='*80}")
            print(f"\nANSWER:\n{answer}")
            print(context_info)
            print(f"{'='*80}\n")
            
            return answer

        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return f"Error querying model: {e}"

    def interactive_session(self):
        """Start interactive Q&A session with the expert."""
        print("\n🧠 Advanced Coding Expert (powered by Llama 2 + RAG)")
        print("Type 'exit' to quit, 'index' to re-index codebase\n")

        while True:
            try:
                question = input("You: ").strip()
                
                if question.lower() == 'exit':
                    print("Goodbye!")
                    break
                
                if question.lower() == 'index':
                    path = input("Enter directory path to index: ").strip()
                    self.rag.index_directory(path)
                    print("✓ Indexing complete")
                    continue
                
                if not question:
                    continue
                
                self.query(question)

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break


if __name__ == "__main__":
    expert = OllamaCodeExpert()
    expert.interactive_session()
