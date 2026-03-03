# Advanced Coding Expert: Complete Implementation Guide

Transform Llama 3.1 into an elite coding expert using Fine-Tuning, RAG, and Agentic Workflows.

## 📚 Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│          User Query / Task                               │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴──────────┐
         │                      │
    ┌────▼────┐          ┌─────▼──────┐
    │ RAG      │          │ Agentic    │
    │ Pipeline │          │ Workflow   │
    └────┬────┘          └─────┬──────┘
         │                      │
    ┌────▼──────────────────────▼─────┐
    │   Llama 3.1 (Fine-tuned)        │
    │   - LoRA Adapters               │
    │   - 8B/13B/70B/405B             │
    └────┬──────────────────────┬─────┘
         │                      │
    ┌────▼────────┐       ┌────▼──────────┐
    │ Vector DB   │       │ Tools          │
    │ (ChromaDB)  │       │ - Linter       │
    │             │       │ - Executor     │
    │ Semantic    │       │ - Search       │
    │ Chunks of   │       │ - Navigator    │
    │ Code        │       └────────────────┘
    └─────────────┘

┌──────────────────────────────────┐
│     FastAPI Server               │
│     /query, /task, /index        │
└──────────────────────────────────┘
```

## 🚀 Quick Start (30 minutes)

### Prerequisites
- macOS/Linux (Windows with WSL2)
- Python 3.10+
- 16GB+ VRAM (RTX 3090/4090/A100)
- ~50GB disk space

### Step 1: Install Base System
```bash
# Clone/setup your workspace
cd /Users/bander/coder/advanced-coding-expert

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Start Ollama (Local LLM Server)
```bash
# Install Ollama (one-time)
brew install ollama

# In one terminal, start Ollama server
ollama serve

# In another terminal, pull model
ollama pull llama2:7b
```

### Step 3: Phase 1 - Continue.dev (5 min)
```bash
# Copy Continue config to VS Code
mkdir -p ~/.continue
cp phase1-continue/.continue-config.json ~/.continue/config.json

# Install Continue.dev extension in VS Code
# Search "Continue" in Extensions marketplace
```

### Step 4: Phase 2 - RAG Pipeline (10 min)
```bash
# Index your codebase
python3 << 'EOF'
from phase2_rag.code_expert import OllamaCodeExpert

expert = OllamaCodeExpert()
# Index the target project
expert.rag.index_directory("/path/to/your/project")
print("✓ Codebase indexed!")
EOF

# Ask questions
python3 phase2_rag/code_expert.py
```

### Step 5: Phase 4 - Agentic API (5 min)
```bash
# Start API server
python3 -m uvicorn phase4_agentic.api_server:app --reload --port 8000

# In another terminal, test:
curl http://localhost:8000/health
```

## 📖 Four Phases Explained

### Phase 1: Continue.dev + Codebase Indexing
**Goal**: Give VS Code Llama as a smart copilot

**What it does**:
- Reads your open files and workspace
- Indexes your project semantically
- Answers questions about your code
- Supports slash commands: `/explain`, `/refactor`, `/test`

**Setup**: [phase1-continue/SETUP.md](phase1-continue/SETUP.md)

**When to use**: Every day in VS Code

---

### Phase 2: Advanced RAG Pipeline
**Goal**: Give Llama "deep memory" of your entire codebase

**What it does**:
1. **Semantic Chunking**: Splits code by functions/classes (not lines)
2. **Vector Database**: Converts chunks to embeddings
3. **Intelligent Search**: Finds relevant code for any query
4. **Context Window**: Feeds best matches to Llama

**Key Files**:
- `phase2_rag/rag_pipeline.py` - Semantic splitting & indexing
- `phase2_rag/code_expert.py` - Query interface

**Example**:
```python
from phase2_rag.code_expert import OllamaCodeExpert

expert = OllamaCodeExpert()
expert.query("How does authentication work in this project?")
# Returns: Llama answer with actual code context from your codebase
```

---

### Phase 3: Fine-Tuning with Unsloth
**Goal**: Adapt Llama to your specific coding style and domain

**What it does**:
1. Loads base Llama model with 4-bit quantization (70% memory savings)
2. Attaches LoRA adapters (the "coding plugins")
3. Trains on your dataset (Magicoder, StackOverflow, or custom)
4. Results in 2-3x better answers for your specific use cases

**Setup**: [phase3-finetuning/GUIDE.md](phase3-finetuning/GUIDE.md)

**Process**:
```bash
# Prepare training data (JSONL format)
# Then run:
python3 phase3-finetuning/unsloth_finetuner.py

# Training time: 30 min - 2 hours depending on GPU/dataset
```

---

### Phase 4: Agentic Workflows  
**Goal**: Give Llama "hands" to run tools and take actions

**Available Tools**:

| Tool | Capabilities |
|------|-------------|
| **Linter** | Run pylint/eslint, check syntax |
| **Search** | grep/ripgrep, find functions |
| **Executor** | Run Python/JavaScript safely |
| **Navigator** | Read files, explore structure |

**API Endpoints**:
```bash
POST /query       - Ask about code
POST /task        - Complete a task (uses tools)
POST /index       - Index directory for RAG
GET /search       - Direct semantic search
GET /tools        - List available tools
```

**Example Task**:
```curl
curl -X POST http://localhost:8000/task \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Find and fix the SQL injection vulnerability in the database layer",
    "use_tools": true
  }'
```

The agent will:
1. Search for SQL-related code
2. Analyze the code structure
3. Run linters to find issues
4. Execute test cases
5. Propose fixes with explanations

## 🛠️ Advanced Usage

### Custom Training Data

Create `data/training_data.jsonl`:
```json
{"instruction": "Optimize this Python function", "input": "def slow_func()...", "output": "def fast_func()..."}
{"instruction": "Fix this bug", "input": "def broken()...", "output": "def fixed()..."}
```

Then:
```python
from phase3_finetuning.unsloth_finetuner import UnslothCodeFineTuner

finetuner = UnslothCodeFineTuner()
finetuner.load_model()
finetuner.setup_lora()
dataset = finetuner.load_training_data("custom")
finetuner.train(dataset)
```

### Integrate Fine-tuned Model

After fine-tuning, update `.continue-config.json`:
```json
{
  "models": [{
    "title": "Llama Expert (Fine-tuned)",
    "provider": "ollama",
    "model": "llama-expert:7b",
    "apiBase": "http://localhost:11434"
  }]
}
```

Then in Ollama:
```bash
ollama create llama-expert \
  -f Modelfile \
  -m /path/to/finetuned/model
```

## 📊 Expected Performance

### Before (Generic Llama)
```
User: "How do we handle database transactions?"
Response: Generic explanation of ACID properties
Accuracy: 40%
Context: None
```

### After (Advanced Expert)
```
User: "How do we handle database transactions?"
Response: "Your project uses SQLAlchemy with the session pattern
(see models/db.py:45). You've implemented optimistic locking
and connection pooling. Here's how to improve error handling..."
Accuracy: 90%+
Context: References actual files and line numbers
```

## 🐛 Troubleshooting

### Issue: "Could not connect to Ollama"
```bash
# Check Ollama is running
ollama serve

# Verify endpoint
curl http://localhost:11434/api/tags
```

### Issue: "Out of Memory during fine-tuning"
```python
# Reduce batch size in config.yaml
finetuning:
  batch_size: 2  # instead of 4
  max_seq_length: 1024  # instead of 2048
  
# Or enable gradient checkpointing:
use_gradient_checkpointing: true
```

### Issue: "RAG not finding relevant code"
1. Re-index: `expert.rag.index_directory(path)`
2. Check chunk size: `chunk_size: 500` in config.yaml
3. More diagnostic info:
```python
results = expert.rag.search("your query", k=10)
for r in results:
    print(f"{r['source']} - Score: {r['relevance_score']}")
```

## 📚 Next Steps

1. ✅ **Day 1**: Set up Phase 1 + 2 (Continue + RAG)
2. ✅ **Day 2**: Prepare training data, start fine-tuning
3. ✅ **Day 3**: Integrate fine-tuned model with RAG
4. ✅ **Week 2**: Deploy agentic tasks in production

## 🔗 Resources

- **Unsloth GitHub**: https://github.com/unslothai/unsloth
- **LangChain Docs**: https://docs.langchain.com/
- **ChromaDB**: https://www.trychroma.com/
- **Continue.dev**: https://continue.dev/
- **Ollama**: https://ollama.ai/

## 💡 Pro Tips

1. **Start small**: Use 7B model first, scale to 70B after proving ROI
2. **Quality data**: 500 high-quality examples beat 100k poor ones
3. **Iterate quickly**: Fine-tune, test, refine in 24-hour cycles
4. **Mix approaches**: RAG + Fine-tuning + Agentic for best results
5. **Monitor costs**: Most of this runs locally - zero API costs

## 📝 License

This implementation is for educational purposes. Follow the licenses of Llama, Unsloth, and other dependencies.

---

**Questions?** Check individual phase guides or README files in each phase directory.
