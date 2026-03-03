# Unsloth Fine-tuning Guide

## Quick Start

### 1. Install Unsloth
```bash
pip install -U unsloth[colab-new]
pip install -U xformers bitsandbytes trl
```

### 2. Load & Train
```python
from unsloth_finetuner import finetune_llama_for_coding

finetuner, trainer = finetune_llama_for_coding()
```

## Available Models

| Model | Size | VRAM | Speed |
|-------|------|------|-------|
| Llama 2 7B | 7B | 16GB | Fast ⚡ |
| Llama 2 13B | 13B | 20GB | Medium |
| Llama 3.1 8B | 8B | 18GB | Fast ⚡ |
| Llama 3.1 70B | 70B | 40GB | Slow |
| Llama 3.1 405B | 405B | 80GB* | Very Slow |

*With Unsloth, 405B fits on A100 with LoRA

## Training Strategy

### Dataset Formats

**Format 1: Instruction-Input-Output**
```json
{
  "instruction": "Write a Python function to...",
  "input": "def example_func():",
  "output": "    return result"
}
```

**Format 2: Prompt-Completion**
```json
{
  "prompt": "def fibonacci(n):",
  "completion": "    if n <= 1: return n\n    return..."
}
```

### Optimal Hyperparameters for Code

```yaml
finetuning:
  lora_r: 8            # 8 = best balance of speed/quality
  lora_alpha: 16       # Usually 2x the r value
  learning_rate: 2e-4  # Standard for LoRA
  batch_size: 4        # Adjust for your VRAM
  num_epochs: 3        # 2-4 epochs usually sufficient
  max_seq_length: 2048 # Code prompts tend to be longer
```

## Memory Optimization

### Before Unsloth (Standard Approach)
- 70B Model: Requires 80GB+ VRAM
- Training Time: 8-12 hours on A100
- Memory Usage: ~100% of VRAM

### With Unsloth
- 70B Model: Fits in 40GB VRAM (50% reduction)
- Training Time: 4-6 hours (2x faster)
- Memory Usage: ~40% savings

### Further Optimization

```python
# Gradient checkpointing (small speed hit, huge memory saving)
use_gradient_checkpointing=True

# 4-bit quantization
load_in_4bit=True
bnb_4bit_use_double_quant=True

# Flash Attention 2 (if supported)
use_flash_attention_2=True
```

## Training Data Best Practices

### 1. Quality Over Quantity
```
Bad: 100k low-quality examples
Good: 10k high-quality, diverse examples from your domain
```

### 2. Balance Code Types
- 40% Function/Method implementations
- 30% Bug fixes and debugging
- 20% Integration and architecture patterns
- 10% Performance optimization examples

### 3. Include Context
```python
# Bad prompt
"Write a function to sort"

# Good prompt
"""
In a Django REST API, write a function to sort products by price and rating.
The function should accept a QuerySet and sorting parameters, returning a sorted QuerySet.
"""
```

## Monitoring Training

```python
# Check loss during training
# Should decrease steadily

# Validate with test set
# Save checkpoints: checkpoint-100, checkpoint-200, etc.

# Use best checkpoint (usually middle one)
# Avoid overfitting (loss on training is great, validation is poor)
```

## Converting to Ollama Format

After fine-tuning, convert to GGUF for Ollama:

```bash
# Install llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make

# Convert Hugging Face model to GGUF
python convert.py path/to/finetuned/model --outfile model.gguf

# Test with Ollama
ollama create coding-expert -f Modelfile
ollama run coding-expert
```

## Expected Improvements

### Before Fine-tuning
```
User: "Optimize this database query"
Model: Generic optimization advice
Relevance: 40%
```

### After Fine-tuning
```
User: "Optimize this database query"
Model: Specific advice for your tech stack
Includes actual code from your patterns
Relevance: 90%+
```

## Troubleshooting

### Out of Memory
1. Reduce `batch_size` → 2
2. Reduce `max_seq_length` → 1024
3. Enable `gradient_checkpointing=True`
4. Quantize to 8-bit instead of 4-bit

### Training Too Slow
1. Increase `batch_size` (if memory allows)
2. Reduce `num_epochs` → 1
3. Use larger model (up to VRAM limit)
4. Check GPU usage: `nvidia-smi`

### Poor Model Quality
1. Check dataset quality (manual review)
2. More diverse training examples
3. Longer training (more epochs)
4. Better prompt formatting
5. Lower learning rate (2e-5 instead of 2e-4)

## Next Steps

1. ✅ Prepare your training dataset
2. ✅ Run fine-tuning script
3. ✅ Test with your codebase
4. ✅ Convert to Ollama format
5. ✅ Integrate with Phase 2 (RAG) for the full system

See `unsloth_finetuner.py` for the complete implementation.
