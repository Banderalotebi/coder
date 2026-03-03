#!/usr/bin/env python3
"""
Setup script for Advanced Coding Expert system
Installs dependencies and initializes the environment
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(cmd, description):
    """Run a shell command and check for errors"""
    print(f"\n📦 {description}...")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ Failed: {description}")
        return False
    print(f"✓ {description}")
    return True


def main():
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   Advanced Coding Expert - Setup                          ║
    ║   Transform Llama 3.1 into a coding specialist            ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

    # Check Python version
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ required")
        sys.exit(1)

    # Create directories
    print("\n📁 Creating directory structure...")
    dirs = ["./data", "./models", "./logs", "./.cache"]
    for d in dirs:
        Path(d).mkdir(exist_ok=True)
    print("✓ Directories created")

    # Install Python dependencies
    if not run_command(
        "pip install --upgrade pip",
        "Upgrading pip"
    ):
        sys.exit(1)

    if not run_command(
        "pip install -r requirements.txt",
        "Installing Python dependencies"
    ):
        sys.exit(1)

    # Create .env file
    if not Path(".env").exists():
        print("\n📝 Creating .env file...")
        with open(".env.example", "r") as src:
            with open(".env", "w") as dst:
                dst.write(src.read())
        print("✓ .env file created (edit with your config)")

    # Check for Ollama
    print("\n🔍 Checking for Ollama...")
    result = subprocess.run("which ollama", shell=True, capture_output=True)
    if result.returncode == 0:
        print("✓ Ollama found")
    else:
        print("❌ Ollama not found. Install with: brew install ollama")
        print("   Then run: ollama pull llama2:7b")

    # Optional: Create Continue config
    print("\n🔧 Setting up Continue.dev...")
    continue_dir = Path.home() / ".continue"
    continue_dir.mkdir(exist_ok=True)
    continue_config = continue_dir / "config.json"
    
    if not continue_config.exists():
        import shutil
        shutil.copy("phase1-continue/.continue-config.json", continue_config)
        print("✓ Continue.dev configured")
    else:
        print("✓ Continue.dev already configured")

    print(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║   Setup Complete! 🎉                                      ║
    ╠═══════════════════════════════════════════════════════════╣
    ║                                                            ║
    ║   Next steps:                                             ║
    ║                                                            ║
    ║   1. Start Ollama:                                        ║
    ║      ollama serve                                         ║
    ║                                                            ║
    ║   2. Pull a model:                                        ║
    ║      ollama pull llama2:7b                                ║
    ║                                                            ║
    ║   3. Start the API server:                                ║
    ║      python -m uvicorn phase4_agentic.api_server:app     ║
    ║                                                            ║
    ║   4. In VS Code, install Continue.dev extension          ║
    ║      and use @codebase in the chat                        ║
    ║                                                            ║
    ║   For detailed instructions, see README.md               ║
    ║                                                            ║
    ╚═══════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    main()
