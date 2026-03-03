#!/bin/bash
# 🧪 Advanced Coding Expert - Complete Testing Guide

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "  HOW TO TEST YOUR ADVANCED CODING EXPERT SYSTEM"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

# Ensure we're in the right directory
cd /Users/bander/coder/advanced-coding-expert

echo "💡 TESTING OPTIONS:"
echo ""
echo "  [1] Quick REST API Test (fastest)"
echo "  [2] Extended Demo (show capabilities)"
echo "  [3] RAG Code Search (semantic search)"
echo "  [4] Agentic Workflows (autonomous tools)"
echo "  [5] Swagger UI (interactive browser)"
echo "  [6] All Tests (run everything)"
echo "  [7] Performance Benchmark"
echo ""
echo "Enter test number (1-7) or 'all':"
read -r choice

case $choice in
  1)
    echo ""
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo "  ✅ TEST 1: QUICK REST API TEST"
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo ""
    echo "🔍 Check 1: API Health"
    echo "Command: curl http://localhost:8000/health"
    echo ""
    curl -s http://localhost:8000/health | jq .
    
    echo ""
    echo "🔍 Check 2: List Available Models"
    echo "Command: curl http://localhost:8000/models"
    echo ""
    curl -s http://localhost:8000/models | jq .
    
    echo ""
    echo "🔍 Check 3: Simple Query"
    echo "Command: curl -X POST http://localhost:8000/query (simple question)"
    echo ""
    curl -s -X POST http://localhost:8000/query \
      -H "Content-Type: application/json" \
      -d '{"question": "What are SOLID principles in OOP?", "temperature": 0.7}' | jq -r '.answer' | head -50
    
    echo ""
    echo "✅ Quick test complete!"
    ;;
  
  2)
    echo ""
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo "  ✅ TEST 2: EXTENDED DEMO (Capabilities)"
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo ""
    ./venv/bin/python demo_phase2.py
    ;;
  
  3)
    echo ""
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo "  ✅ TEST 3: RAG CODE SEARCH (Semantic Search)"
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo ""
    echo "Starting interactive RAG session..."
    echo "This will let you:"
    echo "  • Index your codebase"
    echo "  • Ask questions grounded in YOUR code"
    echo "  • Get expert analysis of specific files"
    echo ""
    ./venv/bin/python phase2-interactive.py
    ;;
  
  4)
    echo ""
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo "  ✅ TEST 4: AGENTIC WORKFLOWS (Autonomous Tools)"
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo ""
    echo "Starting agentic workflows demo..."
    echo "The system will automatically:"
    echo "  • Search for code patterns"
    echo "  • Analyze files"
    echo "  • Lint code"
    echo "  • Execute and analyze results"
    echo ""
    ./venv/bin/python phase4-demo.py
    ;;
  
  5)
    echo ""
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo "  ✅ TEST 5: SWAGGER UI (Interactive Browser)"
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo ""
    echo "Opening interactive API documentation..."
    echo ""
    echo "🌐 Swagger UI: http://localhost:8000/docs"
    echo ""
    echo "You can:"
    echo "  • Try the API endpoints directly"
    echo "  • See request/response schemas"
    echo "  • Test with custom parameters"
    echo ""
    echo "Attempting to open in browser..."
    open http://localhost:8000/docs 2>/dev/null || echo "Open browser manually: http://localhost:8000/docs"
    ;;
  
  6)
    echo ""
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo "  ✅ TEST 6: ALL TESTS (Complete Validation Suite)"
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo ""
    
    echo "Step 1/4: REST API Health Check"
    echo "─────────────────────────────────────────────────────────────"
    curl -s http://localhost:8000/health | jq .
    
    echo ""
    echo "Step 2/4: Expert Model Query"
    echo "─────────────────────────────────────────────────────────────"
    echo "Query: 'Explain the CAP theorem in distributed systems'"
    echo ""
    curl -s -X POST http://localhost:8000/query \
      -H "Content-Type: application/json" \
      -d '{"question": "Explain the CAP theorem in distributed systems", "temperature": 0.7}' | jq -r '.answer' | head -80
    
    echo ""
    echo "Step 3/4: Performance Test"
    echo "─────────────────────────────────────────────────────────────"
    ./venv/bin/python test_expert_llama.py 2>&1 | head -100
    
    echo ""
    echo "Step 4/4: System Inventory"
    echo "─────────────────────────────────────────────────────────────"
    echo "Core components:"
    ls -lh api_simple.py demo_phase2.py phase2-interactive.py phase4-demo.py 2>/dev/null | awk '{print "  ✓", $9, "-", $5}'
    
    echo ""
    echo "✅ All tests completed!"
    ;;
  
  7)
    echo ""
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo "  ✅ TEST 7: PERFORMANCE BENCHMARK"
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo ""
    echo "Running extended output test with performance metrics..."
    echo ""
    ./venv/bin/python test_expert_llama.py
    ;;
  
  *)
    echo "❌ Invalid choice"
    exit 1
    ;;
esac

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "  🎉 Test completed!"
echo "═══════════════════════════════════════════════════════════════════════════════"
