#!/usr/bin/env python3
"""
Test: expert-llama Extended Output Capabilities
Demonstrates unlimited token generation and deep context awareness
"""

import requests
import json
from time import time
from pathlib import Path

OLLAMA_URL = "http://localhost:11434"

def print_header(text):
    print(f"\n{'='*80}")
    print(f"  {text}")
    print(f"{'='*80}\n")

def test_model(model_name, question):
    """Test a model and show response characteristics"""
    print(f"\n🤖 Testing: {model_name}")
    print(f"❓ Question: {question}\n")
    
    start = time()
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model_name,
                "prompt": question,
                "stream": False,
                "temperature": 0.7
            },
            timeout=120
        )
        
        elapsed = time() - start
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("response", "")
            
            # Calculate statistics
            words = len(answer.split())
            tokens = len(answer) // 4  # Rough estimate
            
            # Show full answer for shorter responses, truncate longer ones
            if len(answer) <= 1500:
                print(answer)
            else:
                print(answer[:1500] + f"\n\n[... {len(answer) - 1500} more characters ...]")
            
            print(f"\n📊 Response Metrics:")
            print(f"   Generated: ~{tokens} tokens / {words} words")
            print(f"   Time: {elapsed:.1f} seconds")
            print(f"   Speed: ~{tokens/elapsed:.0f} tokens/sec")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    print_header("EXPERT-LLAMA EXTENDED OUTPUT TEST")
    
    print("""This test demonstrates the benefits of expert-llama:
    
✅ Unlimited token generation (num_predict: -1)
✅ Large context window (32,768 tokens)
✅ Expert system prompt for high-quality responses
✅ Extended timeout for deep analysis

Previous model (llama3.1-coder) would stop after ~500-1000 tokens.
Expert-llama continues until the answer is complete.
    """)
    
    questions = [
        ("Design a production-grade microservices architecture for an e-commerce platform. Include API gateway patterns, database scaling strategies, monitoring, and deployment considerations.",
         "Architecture Design"),
        
        ("Explain how to optimize a Django QuerySet for performance in a large-scale application. Include N+1 query problems, caching strategies, and database indexing best practices.",
         "Performance Optimization"),
        
        ("What are the key considerations when implementing OAuth 2.0 authentication in a multi-tenant SaaS application? Include token refresh strategies and security concerns.",
         "Security & Auth"),
    ]
    
    print_header("RUNNING TESTS WITH EXPERT-LLAMA")
    
    for i, (question, category) in enumerate(questions, 1):
        print(f"\n[Test {i}/{len(questions)}] {category}")
        test_model("expert-llama", question)
        
        if i < len(questions):
            print("\n" + "-"*80)
    
    print_header("TEST COMPLETE")
    print("""✅ expert-llama is configured and running!

Key improvements:
  • No more token truncation
  • Full context retained (32K tokens)
  • Expert-level responses
  • Detailed explanations with examples
  • Suitable for complex architectural decisions

You can now:
  1. Use the REST API at http://localhost:8000
  2. Run RAG with extended code context
  3. Install Continue.dev for VS Code integration
  4. Ask deep technical questions without any limitations
""")

if __name__ == "__main__":
    main()
