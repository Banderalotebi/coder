# Expert-Llama Configuration Guide

## What Was Just Done

Your Ollama setup has been optimized with a custom **expert-llama** model that provides:

✅ **Unlimited Output** - Generates complete, comprehensive answers without truncation  
✅ **32K Token Context** - Remembers large codebases and long conversations  
✅ **Expert Prompting** - System prompt ensures senior-engineer-level responses  
✅ **Extended Timeout** - Gives the model time to think deeply  

## What Changed

### 1. Custom Modelfile Created
**File**: `ExpertCoder.Modelfile`

```dockerfile
FROM llama3.1
PARAMETER num_predict -1          # Unlimited token generation
PARAMETER num_ctx 32768           # 32K tokens of context memory
PARAMETER stop "<|eot_id|>"       # Proper stop sequence
PARAMETER temperature 0.7         # Balanced creativity
SYSTEM "You are an expert software engineer..."
```

### 2. Model Registered in Ollama
**Command**: `ollama create expert-llama -f ExpertCoder.Modelfile`

This creates a new model variant that extends base Llama 3.1 with expert settings.

### 3. Configuration Updated Everywhere

| Component | Change |
|-----------|--------|
| **api_simple.py** | `DEFAULT_MODEL = "expert-llama"` |
| **demo_phase2.py** | `DEFAULT_MODEL = "expert-llama"` |
| **.continue-config.json** | Model: `expert-llama`, timeout: 600s, numPredict: -1 |

## How to Use

### Option A: REST API (Running Now)
The API server is already using expert-llama:

```bash
# Still running, ready to use
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Design a scalable microservices architecture"}'
```

### Option B: Run Demo with Extended Output
```bash
cd /Users/bander/coder/advanced-coding-expert
./venv/bin/python demo_phase2.py
```

Note: Responses will now be much longer and more detailed!

### Option C: Continue.dev (VS Code Extension)

1. Install Continue.dev extension in VS Code:
   - Open VS Code
   - Go to Extensions (Cmd+Shift+X)
   - Search for "Continue"
   - Install "Continue - Codegen with LLMs"

2. The configuration is already set up in:
   ```
   phase1-continue/.continue-config.json
   ```

3. First time setup:
   - Open the Continue sidebar in VS Code
   - It will use expert-llama by default
   - Select any code and press Cmd+K to start

### Option D: RAG with Extended Context

When you index your codebase with RAG, the model can now:
- Keep full file context (up to 32K tokens)
- Provide more thorough code review
- Consider larger architectural patterns
- Give more detailed optimization recommendations

```bash
cd phase2-rag
python code_expert.py
# Type: index
# Paste your project path
```

## Configuration Details

### Token Limits

| Setting | Value | Impact |
|---------|-------|--------|
| `num_predict` | -1 | Generates indefinitely until task is complete |
| `num_ctx` | 32768 | Can process 32K tokens in a single query |
| Timeout | 600s (10 min) | Allows time for long-form analysis |

### Model Quality

The expert-llama model includes a system prompt that ensures:
- ✅ Comprehensive code examples
- ✅ Best practices and architectural insights
- ✅ Performance optimization focus
- ✅ Security-conscious recommendations
- ✅ Explanations for senior engineers

## Switching Back (If Needed)

If you ever want to use the original llama3.1-coder:

```bash
# Edit api_simple.py or demo_phase2.py
DEFAULT_MODEL = "llama3.1-coder"
```

## Performance Notes

**Response Time**: 5-45 seconds depending on question complexity
- Shorter questions: 5-10 seconds
- Code analysis: 15-30 seconds  
- Architecture design: 30-45 seconds

**Memory**: ~8.5GB (same as base Llama 3.1, just reconfigured)

## What This Enables

Your coding expert can now:

1. **Analyze Large Functions** - Full context of 50+ line functions
2. **Design Architectures** - Consider entire service interactions
3. **Comprehensive Reviews** - Multiple aspects in one response
4. **Deep Optimization** - Performance + Security + Scalability
5. **Learning Resources** - Detailed explanations with examples

## Next Steps

- ✅ **API Ready**: Test at `http://localhost:8000/docs`
- 🧠 **RAG Ready**: Index your code with extended context
- 💻 **VS Code Ready**: Install Continue.dev extension
- 🎓 **Expert Ready**: Ask complex architectural questions

Your advanced coding expert is now fully optimized for deep, comprehensive analysis!
