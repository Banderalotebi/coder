#!/bin/bash
# Advanced Coding Expert - Interactive Start Menu

cd /Users/bander/coder/advanced-coding-expert

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Advanced Coding Expert - Ready to Start!                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Choose your next step:"
echo ""
echo "  1) Run demo (see system in action)"
echo "  2) Quick test (verify all systems)"
echo "  3) Start RAG chat (index & search code)"
echo "  4) Start API server (REST interface)"
echo "  5) View full documentation"
echo ""
read -p "Enter choice (1-5): " choice

case $choice in
  1)
    echo ""
    ./venv/bin/python demo.py
    ;;
  2)
    echo ""
    ./venv/bin/python quick_test.py
    ;;
  3)
    echo ""
    echo "📝 Starting RAG Chat System..."
    echo "When ready, type: index /path/to/your/project"
    echo ""
    cd phase2-rag
    ../../venv/bin/python code_expert.py
    ;;
  4)
    echo ""
    echo "🌐 Starting API Server..."
    echo "Server: http://localhost:8000"
    echo "Docs:   http://localhost:8000/docs"
    echo ""
    ./venv/bin/python -m uvicorn phase4-agentic.api_server:app --reload
    ;;
  5)
    cat SYSTEM_READY.txt
    ;;
  *)
    echo "Showing system status..."
    cat SYSTEM_READY.txt
    ;;
esac
