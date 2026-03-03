# Phase 1: Continue.dev Integration with Codebase Indexing

continue.json should be placed in your VS Code workspace:

```json
{
  "models": [
    {
      "title": "Ollama Local - Llama2",
      "provider": "ollama",
      "model": "llama2:7b",
      "apiBase": "http://localhost:11434"
    }
  ],
  "contextProviders": [
    {
      "name": "codebase"
    },
    {
      "name": "file"
    },
    {
      "name": "search"
    }
  ],
  "slashCommands": [
    {
      "name": "explain",
      "description": "Explain the selected code"
    },
    {
      "name": "refactor",
      "description": "Refactor the selected code"
    },
    {
      "name": "test",
      "description": "Generate tests for selected code"
    },
    {
      "name": "debug",
      "description": "Debug the selected code"
    }
  ],
  "disableIndexing": false
}
```

## Installation Steps:

1. **Install Continue.dev Extension in VS Code:**
   - Open VS Code
   - Go to Extensions (Cmd+Shift+X)
   - Search for "Continue"
   - Install the official Continue.dev extension

2. **Install Ollama (Local LLM Server):**
   ```bash
   # macOS
   brew install ollama
   
   # Or download from: https://ollama.ai
   ```

3. **Pull Llama 2 Model:**
   ```bash
   ollama pull llama2:7b
   # or for better performance: ollama pull llama2:13b
   ```

4. **Start Ollama:**
   ```bash
   ollama serve
   # Runs on http://localhost:11434
   ```

5. **Configure Continue.dev:**
   - Create `.continue/config.json` in your workspace
   - Copy the configuration above
   - Reload VS Code

6. **Enable Codebase Indexing:**
   - In VS Code, run: `Continue: Index Codebase`
   - This will scan your files and create semantic index
   - You can now use `@codebase` in Continue chat

## Usage:
- Open Continue sidebar (Cmd+Shift+C)
- Use `@codebase` to reference your entire project
- Ask questions like: "How is error handling implemented here?"
- Use slash commands: `/explain`, `/refactor`, `/test`, `/debug`
