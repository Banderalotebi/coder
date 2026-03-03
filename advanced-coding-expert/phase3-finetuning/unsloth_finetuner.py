"""
Phase 3: Fine-tuning Llama 3.1 with Unsloth
Adapts the base model to become a specialized coding expert.

Requirements:
- GPU with at least 16GB VRAM (RTX 3090, 4090, A100, etc.)
- Install with: pip install -e .[colab-new]
"""

import os
from typing import Optional, Dict, List
import json
import logging
from pathlib import Path

from unsloth import FastLanguageModel, unsloth_train_template
from datasets import load_dataset, Dataset
import torch
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer, TrainingArguments
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UnslothCodeFineTuner:
    """
    Fine-tunes Llama with Unsloth for 2x speed + 70% memory savings.
    Uses LoRA (Low-Rank Adaptation) for efficient tuning.
    """

    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.model = None
        self.tokenizer = None
        
    def _load_config(self, path: str) -> dict:
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def load_model(self, model_id: str = "unsloth/llama-2-7b-bnb-4bit"):
        """
        Load Llama model with 4-bit quantization (saves memory).
        
        Available models:
        - "unsloth/llama-2-7b-bnb-4bit"         (7B)
        - "unsloth/llama-2-13b-bnb-4bit"        (13B - recommended)
        - "unsloth/Llama-3.1-8B-bnb-4bit"       (Llama 3.1 8B)
        - "unsloth/Llama-3-70b-bnb-4bit"        (70B)
        """
        logger.info(f"Loading model: {model_id}")
        
        max_seq_length = self.config['finetuning']['max_seq_length']
        
        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name=model_id,
            max_seq_length=max_seq_length,
            dtype=torch.float16,
            load_in_4bit=True,
        )
        
        logger.info("✓ Model loaded successfully with 4-bit quantization")

    def setup_lora(self):
        """
        Attach LoRA adapters (the "coding plugins").
        """
        lora_config = self.config['finetuning']
        
        self.model = FastLanguageModel.get_peft_model(
            self.model,
            r=lora_config['lora_r'],
            lora_alpha=lora_config['lora_alpha'],
            lora_dropout=lora_config['lora_dropout'],
            target_modules=["q_proj", "v_proj"],  # Key attention layers
            bias="none",
            use_gradient_checkpointing=True,
            use_rslora=True,
        )
        
        logger.info(f"✓ LoRA configured: r={lora_config['lora_r']}, alpha={lora_config['lora_alpha']}")

    def load_training_data(
        self,
        dataset_name: str = "magicoder",
        split: str = "train",
        num_samples: Optional[int] = None
    ) -> Dataset:
        """
        Load training dataset from Hugging Face.
        
        Recommended datasets for coding:
        - "magicoder": High-quality code generation examples
        - "stack_code_search": Real code with natural queries
        - "Your custom dataset": Upload to HF Hub
        """
        logger.info(f"Loading dataset: {dataset_name}")
        
        # For this example, we'll use a smaller dataset or custom format
        if dataset_name == "magicoder":
            # Note: Install with: pip install datasets
            dataset = load_dataset("ise-uiuc/Magicoder-OSS-Control-Instruct")
            dataset = dataset[split]
        elif dataset_name == "custom":
            # For custom datasets, load from local JSONL/JSON
            dataset = load_dataset("json", data_files="./data/training_data.jsonl")
        else:
            dataset = load_dataset(dataset_name, split=split)

        if num_samples:
            dataset = dataset.select(range(min(num_samples, len(dataset))))

        logger.info(f"✓ Loaded {len(dataset)} training examples")
        return dataset

    def prepare_dataset(self, dataset: Dataset) -> Dataset:
        """
        Format dataset for instruction fine-tuning.
        Ensures consistent prompt format for the model.
        """
        
        def format_instruction(example):
            """Convert dataset examples to instruction format."""
            
            # Adjust these fields based on your dataset structure
            if "instruction" in example:
                instruction = example.get("instruction", "")
                input_text = example.get("input", "")
                output_text = example.get("output", "")
            else:
                # Fallback for datasets with different formats
                instruction = example.get("prompt", example.get("question", ""))
                output_text = example.get("completion", example.get("answer", ""))
                input_text = ""

            prompt = f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{instruction}

### Input:
{input_text}

### Response:
{output_text}"""

            return {"text": prompt}

        # Map formatting function
        formatted_dataset = dataset.map(
            format_instruction,
            remove_columns=dataset.column_names,
            desc="Formatting dataset"
        )

        return formatted_dataset

    def train(
        self,
        dataset: Dataset,
        output_dir: Optional[str] = None,
        num_epochs: Optional[int] = None,
    ):
        """
        Fine-tune the model with the prepared dataset.
        """
        if output_dir is None:
            output_dir = self.config['finetuning']['output_dir']
        if num_epochs is None:
            num_epochs = self.config['finetuning']['num_epochs']

        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=self.config['finetuning']['batch_size'],
            gradient_accumulation_steps=4,
            warmup_steps=5,
            max_steps=100,  # Adjust based on dataset size
            learning_rate=self.config['finetuning']['learning_rate'],
            fp16=True,  # Use float16 for memory efficiency
            logging_strategy="steps",
            logging_steps=10,
            save_strategy="steps",
            save_steps=20,
            optim="adamw_8bit",  # Memory-efficient optimizer
            seed=42,
        )

        trainer = SFTTrainer(
            model=self.model,
            tokenizer=self.tokenizer,
            train_dataset=dataset,
            dataset_text_field="text",
            max_seq_length=self.config['finetuning']['max_seq_length'],
            args=training_args,
        )

        logger.info("🚀 Starting fine-tuning...")
        trainer.train()

        logger.info(f"✓ Fine-tuning complete! Model saved to {output_dir}")
        return trainer

    def save_model(self, output_dir: str):
        """Save fine-tuned model and tokenizer."""
        logger.info(f"Saving model to {output_dir}")
        
        # Save LoRA weights
        self.model.save_pretrained(output_dir)
        self.tokenizer.save_pretrained(output_dir)
        
        logger.info(f"✓ Model saved successfully")

    def export_gguf(self, output_path: str):
        """
        Export model to GGUF format for Ollama/llama.cpp.
        Enables running on CPU.
        """
        logger.info(f"Exporting to GGUF format...")
        # This requires additional setup with llama.cpp
        # See: https://github.com/ggerganov/llama.cpp
        logger.info("Note: GGUF export requires llama.cpp tools")


def finetune_llama_for_coding():
    """
    Complete fine-tuning pipeline.
    """
    
    # Initialize
    finetuner = UnslothCodeFineTuner("config.yaml")
    
    # Load model
    finetuner.load_model("unsloth/llama-2-7b-bnb-4bit")
    
    # Setup LoRA
    finetuner.setup_lora()
    
    # Load dataset
    dataset = finetuner.load_training_data("magicoder")
    
    # Prepare dataset
    formatted_dataset = finetuner.prepare_dataset(dataset)
    
    # Train
    trainer = finetuner.train(formatted_dataset)
    
    # Save
    finetuner.save_model("./models/llama-coding-expert")
    
    return finetuner, trainer


if __name__ == "__main__":
    # For GPU memory optimization tips:
    print("""
    GPU OPTIMIZATION TIPS:
    ✓ Unsloth reduces memory by 70% compared to standard training
    ✓ With RTX 3090 (24GB): Can train 70B model with LoRA
    ✓ With RTX 4090 (24GB): Can train 405B model with LoRA
    ✓ With A100 (80GB): Can train very large models with full fine-tuning
    
    COMMON ISSUES:
    - Out of Memory: Reduce batch_size or max_seq_length
    - Slow training: GPU not detected. Check: nvidia-smi
    - Import errors: pip install unsloth[colab-new] -U
    """)
    
    # Uncomment to start training:
    # finetuner, trainer = finetune_llama_for_coding()
