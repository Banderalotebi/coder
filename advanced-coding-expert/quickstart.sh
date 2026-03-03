#!/bin/bash
# Advanced Coding Expert - Quick Start Script
# Runs all initialization steps automatically

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   Advanced Coding Expert - Automated Setup                     ║"
echo "║   Building Elite Llama 3.1 Coding System                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Python $python_version detected"

# Create virtual environment if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "📦 Installing dependencies (this may take 5-10 minutes)..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1

# Install core dependencies first
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu > /dev/null 2>&1

# Install remaining dependencies
pip install -r requirements.txt

echo "✓ All dependencies installed"

# Create necessary directories
echo ""
echo "📁 Creating directories..."
mkdir -p data models logs .cache
echo "✓ Directories created"

# Copy environment file
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created (edit with your token/config)"
fi

# Setup Continue.dev
echo ""
echo "🔧 Configuring Continue.dev..."
mkdir -p ~/.continue
if ! [ -f ~/.continue/config.json ]; then
    cp phase1-continue/.continue-config.json ~/.continue/config.json
    echo "✓ Continue.dev configured"
else
    echo "✓ Continue.dev already configured"
fi

# Check for Ollama
echo ""
echo "🔍 Checking for Ollama..."
if command -v ollama &> /dev/null; then
    echo "✓ Ollama found at: $(which ollama)"
else
    echo "❌ Ollama not found"
    echo "   Install with: brew install ollama"
    echo "   Then: ollama pull llama2:7b"
    echo ""
fi

# Summary
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   Setup Complete! ✨                                           ║"
echo "╠════════════════════════════════════════════════════════════════╣"
echo "║                                                                 ║"
echo "║  Next Steps:                                                   ║"
echo "║                                                                ║"
echo "║  1️⃣  Start Ollama (in separate terminal):                      ║"
echo "║     ollama serve                                               ║"
echo "║                                                                 ║"  
echo "║  2️⃣  Pull a model:                                             ║"
echo "║     ollama pull llama2:7b                                      ║"
echo "║                                                                 ║"
echo "║  3️⃣  Start the API server:                                    ║"
echo "║     python -m uvicorn phase4_agentic.api_server:app            ║"
echo "║                                                                 ║"
echo "║  4️⃣  In VS Code:                                               ║"
echo "║     - Install Continue.dev extension                           ║"
echo "║     - Use @codebase in chat                                    ║"
echo "║                                                                 ║"
echo "║  5️⃣  Index your codebase:                                      ║"
echo "║     python phase2_rag/code_expert.py                           ║"
echo "║     Then type: index /path/to/project                          ║"
echo "║                                                                 ║"
echo "║  📚 For detailed help, see:                                    ║"
echo "║     - README.md (overview)                                     ║"
echo "║     - QUICK_REFERENCE.md (commands)                            ║"
echo "║     - docs/IMPLEMENTATION.md (technical)                       ║"
echo "║                                                                 ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
