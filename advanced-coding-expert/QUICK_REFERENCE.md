# Advanced Coding Expert - Quick Reference

## Installation (30 seconds)

```bash
cd /Users/bander/coder/advanced-coding-expert
python3 setup.py
```

## Essential Commands

### Start Ollama
```bash
ollama serve
# In another terminal:
ollama pull llama2:7b
```

### Start RAG + API Server
```bash
python -m uvicorn phase4_agentic.api_server:app --reload
```

### Interactive RAG Chat
```bash
python phase2_rag/code_expert.py
```

### Index Your Codebase
```python
from phase2_rag.code_expert import OllamaCodeExpert
expert = OllamaCodeExpert()
expert.rag.index_directory("/path/to/project")
```

### Query via API
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How does auth work?"}'
```

### Complete a Task with Tools
```bash
curl -X POST http://localhost:8000/task \
  -H "Content-Type: application/json" \
  -d '{"task": "Find SQL injection bugs", "use_tools": true}'
```

## File Structure

```
advanced-coding-expert/
├── README.md                    # Main guide
├── config.yaml                  # Configuration
├── requirements.txt             # Dependencies
├── setup.py                     # Setup script
├── examples.py                  # Code examples
│
├── phase1-continue/             # Continue.dev integration
│   ├── SETUP.md
│   └── .continue-config.json
│
├── phase2-rag/                  # RAG pipeline
│   ├── rag_pipeline.py         # Semantic splitting & search
│   └── code_expert.py          # RAG + LLM interface
│
├── phase3-finetuning/          # Unsloth fine-tuning
│   ├── unsloth_finetuner.py   # Training script
│   └── GUIDE.md
│
├── phase4-agentic/             # Tool use & automation
│   ├── agentic_tools.py       # Tool definitions
│   └── api_server.py          # FastAPI server
│
└── docs/                       # Documentation
    ├── IMPLEMENTATION.md       # Technical details
    └── QUICK_REFERENCE.md      # This file
```

## Key Concepts

**RAG** (Retrieval-Augmented Generation)
- Semantic search of your codebase
- Feeds relevant code to LLM
- Result: Expert answers with real code context

**LoRA** (Low-Rank Adaptation)
- Lightweight fine-tuning technique
- 1000x fewer trainable parameters
- 70% less memory required

**Agentic** (Tool-Using Agent)
- Model can search code, run linters, execute tests
- Self-correcting: sees errors and fixes them
- More capable than standard chat

**Unsloth**
- 2x faster training
- 70% less memory
- Same quality as standard approach

## Common Tasks

**Task**: Answer question about codebase
```python
from phase2_rag.code_expert import OllamaCodeExpert
expert = OllamaCodeExpert()
expert.query("How is user authentication implemented?")
```

**Task**: Find bugs automatically
```python
from phase4_agentic.agentic_tools import CodeAgent
agent = CodeAgent()
agent.process_task("Find and fix security vulnerabilities")
```

**Task**: Fine-tune on your code style
```python
from phase3_finetuning.unsloth_finetuner import UnslothCodeFineTuner
finetuner = UnslothCodeFineTuner()
finetuner.load_model()
finetuner.setup_lora()
dataset = finetuner.load_training_data("your_dataset")
finetuner.train(dataset)
```

**Task**: Integrate with VS Code
- Install Continue.dev extension
- Copy config from phase1-continue/
- Start Ollama
- Use @codebase in Continue chat

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Ollama connection refused" | Run `ollama serve` in another terminal |
| "Model not found" | Run `ollama pull llama2:7b` |
| "Out of memory" | Reduce batch_size in config.yaml |
| "RAG search too slow" | Increase chunk_size |
| "Poor answer quality" | Re-index codebase or fine-tune |

## Performance Tips

1. **Fast responses**: Use 7B model + small chunk_size
2. **Quality answers**: Use 13B model + full RAG context
3. **GPU memory**: Quantize to 4-bit (Unsloth does this)
4. **Training speed**: Unsloth is 2x faster by default
5. **Search quality**: Aim for 0.7+ relevance score

## Resource Requirements

| Component | VRAM | CPU | Storage |
|-----------|------|-----|---------|
| Llama 7B | 6GB | 2 cores | 4GB |
| Llama 13B | 10GB | 4 cores | 7GB |
| RAG Index | 2-4GB | 2 cores | 5-20GB |
| Fine-tuning 7B | 16GB | 8 cores | 20GB |
| Fine-tuning 13B | 24GB | 12 cores | 30GB |

## API Reference

### /query (RAG)
```bash
POST /query
{
  "question": "How does this work?",
  "use_rag": true,
  "temperature": 0.7
}
```

### /task (Agentic)
```bash
POST /task
{
  "task": "Fix the bug",
  "use_tools": true,
  "max_iterations": 5
}
```

### /index (Indexing)
```bash
POST /index
{
  "directory": "/path/to/project",
  "file_patterns": [".py", ".ts"]
}
```

### /search (Direct)
```bash
GET /search?q=database&k=5
```

## Getting Help

- **Phase-specific questions**: See phase*/README.md
- **Technical details**: See docs/IMPLEMENTATION.md
- **Code examples**: See examples.py
- **API docs**: http://localhost:8000/docs

## Next Steps

1. Run setup.py
2. Start Ollama + pull model
3. Index your codebase
4. Try /query endpoint
5. Fine-tune on your style (optional)
6. Deploy agentic workflows

Good luck! 🚀
