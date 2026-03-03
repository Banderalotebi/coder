#!/usr/bin/env python3
"""
Phase 4: Agentic Workflows Demo
Shows the expert system using autonomous tools to analyze code
"""

import requests
import json
from pathlib import Path
from typing import Optional
import subprocess

OLLAMA_URL = "http://localhost:11434"
EXPERT_MODEL = "expert-llama"
API_URL = "http://localhost:8000"

def print_header(text):
    print(f"\n{'='*80}")
    print(f"  {text}")
    print(f"{'='*80}\n")

def print_tool(tool_name, result):
    """Pretty print tool results"""
    print(f"\n🔧 [{tool_name}]")
    print(json.dumps(result, indent=2))

def linter_tool(filepath: str):
    """Run pylint on a Python file"""
    try:
        result = subprocess.run(
            ["pylint", filepath, "--disable=all", "--enable=E,F"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return {
            "tool": "pylint",
            "file": filepath,
            "errors": result.stdout[:500] if result.stdout else "No errors",
            "status": "success" if result.returncode == 0 else "issues_found"
        }
    except Exception as e:
        return {
            "tool": "pylint",
            "file": filepath,
            "error": str(e),
            "status": "failed"
        }

def search_tool(pattern: str, directory: str = "."):
    """Search for code patterns using grep"""
    try:
        result = subprocess.run(
            ["grep", "-r", pattern, directory, "--include=*.py"],
            capture_output=True,
            text=True,
            timeout=10
        )
        lines = result.stdout.strip().split('\n')[:5] if result.stdout else []
        return {
            "tool": "search",
            "pattern": pattern,
            "matches": len(lines),
            "results": lines,
            "status": "success"
        }
    except Exception as e:
        return {
            "tool": "search",
            "pattern": pattern,
            "error": str(e),
            "status": "failed"
        }

def navigator_tool(filepath: str):
    """Read file content with line numbers"""
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        # Show first 30 lines
        content = ''.join(lines[:30])
        return {
            "tool": "navigator",
            "file": filepath,
            "lines_total": len(lines),
            "content": content,
            "status": "success"
        }
    except Exception as e:
        return {
            "tool": "navigator",
            "file": filepath,
            "error": str(e),
            "status": "failed"
        }

def executor_tool(code: str, language: str = "python"):
    """Execute code snippet safely"""
    try:
        if language == "python":
            result = subprocess.run(
                ["python", "-c", code],
                capture_output=True,
                text=True,
                timeout=5
            )
            return {
                "tool": "executor",
                "language": language,
                "output": result.stdout[:500],
                "error": result.stderr[:500] if result.stderr else None,
                "status": "success" if result.returncode == 0 else "error"
            }
    except Exception as e:
        return {
            "tool": "executor",
            "language": language,
            "error": str(e),
            "status": "failed"
        }

def agent_task(task_description: str, tools_to_use: list):
    """Execute an agentic task"""
    print(f"\n📋 Task: {task_description}")
    print(f"🔧 Using tools: {', '.join(tools_to_use)}\n")
    
    results = {}
    
    # Execute tools based on task
    if "lint" in task_description.lower() and "linter" in tools_to_use:
        results["linter"] = linter_tool("api_simple.py")
        print_tool("Pylint", results["linter"])
    
    if "search" in task_description.lower() and "search" in tools_to_use:
        pattern = "def query" if "query" in task_description.lower() else "class"
        results["search"] = search_tool(pattern)
        print_tool("Search", results["search"])
    
    if "read" in task_description.lower() and "navigator" in tools_to_use:
        results["navigator"] = navigator_tool("api_simple.py")
        print_tool("Navigator", results["navigator"])
    
    # Now ask expert to analyze tool results
    print("\n🤖 Expert-llama analyzing tool results...\n")
    
    tool_context = json.dumps(results, indent=2)
    prompt = f"""You are analyzing tool results from a code analysis task.

Task: {task_description}

Tool Results:
{tool_context}

Provide a concise analysis of what the tools found and any recommendations."""
    
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": EXPERT_MODEL,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7
            },
            timeout=60
        )
        
        if response.status_code == 200:
            analysis = response.json().get("response", "")
            if len(analysis) > 800:
                print(analysis[:800] + "\n\n[... analysis continues ...]")
            else:
                print(analysis)
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Error querying expert: {str(e)}")

def demo_flow():
    """Demonstrate agentic workflow"""
    print_header("PHASE 4 DEMO: AGENTIC WORKFLOWS")
    
    print("""Agentic workflows let your expert system:
    
✅ Automatically lint code for errors
✅ Search codebase for patterns
✅ Read and analyze files
✅ Execute code snippets
✅ Combine results for intelligent recommendations

The expert model uses tool results to provide context-aware analysis.
    """)
    
    # Check if API is running
    try:
        resp = requests.get(f"{API_URL}/", timeout=2)
        print("✅ API running on http://localhost:8000")
    except:
        print("⚠️  API not running. Start it with:")
        print("   cd /Users/bander/coder/advanced-coding-expert")
        print("   ./venv/bin/python api_simple.py &")
    
    print("\n" + "="*80)
    
    # Task 1: Code analysis
    print("\n[Task 1] Analyze API code quality")
    agent_task(
        "Check the API server code for linting issues and provide recommendations",
        ["linter", "navigator"]
    )
    
    # Task 2: Pattern search
    print("\n" + "="*80)
    print("\n[Task 2] Find all query functions")
    agent_task(
        "Search for all function definitions and show what query functions exist",
        ["search", "navigator"]
    )
    
    # Task 3: Integration test
    print("\n" + "="*80)
    print("\n[Task 3] Test the query endpoint")
    agent_task(
        "Execute a simple test of the query endpoint",
        ["executor"]
    )

def interactive_agent():
    """Interactive agentic workflow"""
    print_header("PHASE 4: INTERACTIVE AGENTIC AGENT")
    
    print("""Commands:
  • task <description> - Ask the agent to do something
  • lint <file> - Run linter on file
  • search <pattern> - Search for pattern
  • read <file> - Read file content
  • exec <code> - Execute Python code
  • exit - Quit
""")
    
    while True:
        try:
            cmd = input("\n> ").strip()
            
            if cmd.lower() == 'exit':
                print("Goodbye!")
                break
            
            elif cmd.lower().startswith('task '):
                description = cmd[5:].strip()
                agent_task(description, ["linter", "search", "navigator"])
            
            elif cmd.lower().startswith('lint '):
                filepath = cmd[5:].strip()
                result = linter_tool(filepath)
                print_tool("Pylint", result)
            
            elif cmd.lower().startswith('search '):
                pattern = cmd[7:].strip()
                result = search_tool(pattern)
                print_tool("Search", result)
            
            elif cmd.lower().startswith('read '):
                filepath = cmd[5:].strip()
                result = navigator_tool(filepath)
                print_tool("Navigator", result)
            
            elif cmd.lower().startswith('exec '):
                code = cmd[5:].strip()
                result = executor_tool(code)
                print_tool("Executor", result)
            
            else:
                print("❓ Unknown command. Type 'exit' to quit.")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break

def main():
    print_header("PHASE 4: AGENTIC WORKFLOWS")
    
    print("""What are Agentic Workflows?
    
Agentic = The system acts autonomously using tools
Workflows = Chain of tool calls to solve a problem

Your expert system can now:
  🔧 Lint code automatically
  🔍 Search your codebase
  📄 Read and navigate files
  ⚙️  Execute code safely
  🧠 Analyze results intelligently
    """)
    
    print("Choose a mode:")
    print("  1) Demo (automated workflow examples)")
    print("  2) Interactive (manual tool usage)")
    print("  3) Skip to next phase")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        demo_flow()
        print_header("DEMO COMPLETE")
        print("""✅ You've seen Phase 4 in action!

Next steps:
  • Use interactive mode to explore your own code
  • Deploy to production with REST API
  • Configure CI/CD integration
  • Add custom tools for your workflow
""")
    elif choice == '2':
        interactive_agent()
    elif choice == '3':
        print("\nMoving to summary...")
        return
    else:
        print("Invalid choice")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
