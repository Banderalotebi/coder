"""
Quick start examples for Advanced Coding Expert
"""

# Example 1: Query with RAG
from phase2_rag.code_expert import OllamaCodeExpert

expert = OllamaCodeExpert()

# Index your project once
# expert.rag.index_directory("/path/to/project")

# Ask questions
expert.query("How is error handling implemented?")
expert.query("Show me the authentication flow")
expert.query("What are the performance bottlenecks?")


# Example 2: Use agentic tools
from phase4_agentic.agentic_tools import CodeAgent

agent = CodeAgent()
agent.process_task("Find SQL injection vulnerabilities in database code")


# Example 3: Fine-tune on your dataset
from phase3_finetuning.unsloth_finetuner import UnslothCodeFineTuner

finetuner = UnslothCodeFineTuner()
finetuner.load_model("unsloth/llama-2-7b-bnb-4bit")
finetuner.setup_lora()

# Your training data
dataset = finetuner.load_training_data("magicoder")
formatted = finetuner.prepare_dataset(dataset)
trainer = finetuner.train(formatted)
finetuner.save_model("./models/llama-expert")


# Example 4: API Usage
import requests

BASE_URL = "http://localhost:8000"

# Index codebase
requests.post(f"{BASE_URL}/index", json={
    "directory": "/path/to/project",
    "file_patterns": [".py", ".ts"]
})

# Ask question
requests.post(f"{BASE_URL}/query", json={
    "question": "How do we handle transactions?",
    "use_rag": True
})

# Complete task
requests.post(f"{BASE_URL}/task", json={
    "task": "Optimize the slow API endpoint",
    "use_tools": True
})

# Search directly
requests.get(f"{BASE_URL}/search?q=database%20connection&k=5")
