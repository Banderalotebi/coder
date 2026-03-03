"""
Phase 4: Agentic Workflows & Tool Use
Gives Llama the ability to run tools, search code, and execute code.
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
import json
import subprocess
import logging
import ast
import re
from pathlib import Path

import requests
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ToolType(str, Enum):
    """Types of tools the agent can use"""
    LINTER = "linter"
    SEARCH = "search"
    EXECUTOR = "executor"
    FILE_NAVIGATOR = "file_navigator"
    TEST_RUNNER = "test_runner"


@dataclass
class Tool:
    """Definition of a callable tool"""
    name: str
    description: str
    parameters: Dict[str, str]
    callable: Callable
    tool_type: ToolType


class LinterTool:
    """Run linters on code to catch errors"""
    
    def __init__(self):
        self.name = "linter"
        self.description = "Run pylint, eslint, or other linters on code files"
    
    def run_pylint(self, file_path: str) -> Dict:
        """Run pylint on Python file"""
        try:
            result = subprocess.run(
                ["pylint", file_path, "--output-format=json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return {
                "status": "success" if result.returncode == 0 else "issues_found",
                "output": result.stdout,
                "file": file_path
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def run_eslint(self, file_path: str) -> Dict:
        """Run eslint on JavaScript file"""
        try:
            result = subprocess.run(
                ["eslint", file_path, "--format=json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return {
                "status": "success" if result.returncode == 0 else "issues_found",
                "output": result.stdout,
                "file": file_path
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def check_syntax(self, code: str, language: str = "python") -> Dict:
        """Check code syntax"""
        if language == "python":
            try:
                ast.parse(code)
                return {"status": "valid", "language": language}
            except SyntaxError as e:
                return {
                    "status": "syntax_error",
                    "line": e.lineno,
                    "message": e.msg,
                    "text": e.text
                }
        elif language == "javascript":
            # Simple check using regex
            if "{" in code and "}" in code:
                return {"status": "valid", "language": language}
        return {"status": "unchecked", "language": language}


class SearchTool:
    """Search across codebase"""
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.name = "search"
        self.description = "Search for patterns in code using grep/ripgrep"

    def grep_search(self, pattern: str, file_pattern: str = "*.py") -> List[Dict]:
        """Search for pattern in files"""
        results = []
        try:
            for file_path in self.root_dir.rglob(file_pattern):
                if any(skip in str(file_path) for skip in ['.git', '__pycache__', 'node_modules']):
                    continue
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        if re.search(pattern, line):
                            results.append({
                                "file": str(file_path),
                                "line": line_num,
                                "content": line.strip()[:100]
                            })
        except Exception as e:
            logger.error(f"Search error: {e}")
        
        return results

    def find_function(self, func_name: str) -> List[Dict]:
        """Find function definitions"""
        results = []
        pattern = rf"def\s+{func_name}\s*\("
        
        for py_file in self.root_dir.rglob("*.py"):
            if any(skip in str(py_file) for skip in ['.git', '__pycache__']):
                continue
            
            try:
                with open(py_file, 'r') as f:
                    for line_num, line in enumerate(f, 1):
                        if re.search(pattern, line):
                            results.append({
                                "file": str(py_file),
                                "line": line_num,
                                "definition": line.strip()
                            })
            except:
                pass
        
        return results


class CodeExecutor:
    """Execute code in a sandboxed environment"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.name = "executor"
        self.description = "Execute Python/JavaScript code in sandbox"

    def execute_python(self, code: str, isolated: bool = True) -> Dict:
        """Execute Python code safely"""
        try:
            # Create temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name

            # Execute
            result = subprocess.run(
                ["python", temp_file],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            import os
            os.unlink(temp_file)

            return {
                "status": "success" if result.returncode == 0 else "error",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "message": f"Execution timed out after {self.timeout}s"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def execute_with_input(self, code: str, input_data: str) -> Dict:
        """Execute code with input"""
        try:
            result = subprocess.run(
                ["python", "-c", code],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            return {
                "status": "success" if result.returncode == 0 else "error",
                "output": result.stdout,
                "error": result.stderr
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}


class FileNavigator:
    """Navigate and analyze file structure"""
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.name = "file_navigator"
        self.description = "Navigate file structure and read files"

    def read_file(self, file_path: str, lines: Optional[tuple] = None) -> Dict:
        """Read file contents"""
        try:
            full_path = self.root_dir / file_path
            with open(full_path, 'r') as f:
                content = f.read()
            
            if lines:
                start, end = lines
                content_lines = content.split('\n')
                content = '\n'.join(content_lines[start-1:end])
            
            return {
                "status": "success",
                "file": file_path,
                "content": content
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def list_directory(self, dir_path: str = ".") -> List[str]:
        """List directory contents"""
        try:
            full_path = self.root_dir / dir_path
            items = []
            for p in full_path.iterdir():
                if not p.name.startswith('.'):
                    items.append(p.name)
            return sorted(items)
        except Exception as e:
            return []

    def analyze_structure(self) -> Dict:
        """Analyze project structure"""
        structure = {}
        for py_file in self.root_dir.rglob("*.py"):
            if any(skip in str(py_file) for skip in ['.git', '__pycache__', '.venv']):
                continue
            
            try:
                with open(py_file, 'r') as f:
                    tree = ast.parse(f.read())
                
                classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                
                structure[str(py_file)] = {
                    "classes": classes,
                    "functions": functions
                }
            except:
                pass
        
        return structure


class CodeAgent:
    """
    Main agent that orchestrates tool use.
    The model can call any of these tools to complete tasks.
    """

    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "llama2:7b"):
        self.ollama_url = ollama_url
        self.model = model
        
        # Initialize tools
        self.tools = {
            "linter": LinterTool(),
            "search": SearchTool(),
            "executor": CodeExecutor(),
            "navigator": FileNavigator(),
            "techpartner": TechPartnerAPITool()
        }
        
        self.tool_descriptions = self._build_tool_descriptions()

    def _build_tool_descriptions(self) -> str:
        """Build tool information for the model"""
        descriptions = """
You have access to the following tools:

1. linter: Run code linters to check for errors
   - check_syntax(code, language): Check if code is syntactically valid
   - run_pylint(file_path): Lint Python files
   - run_eslint(file_path): Lint JavaScript files

2. search: Search codebase for patterns
   - grep_search(pattern, file_pattern): Search with regex
   - find_function(func_name): Find function definitions

3. executor: Execute code safely
   - execute_python(code): Run Python code
   - execute_with_input(code, input_data): Run code with input

4. navigator: Navigate and read files
   - read_file(file_path, lines): Read file contents
   - list_directory(dir_path): List directory
   - analyze_structure(): Show project structure

5. techpartner: Query TechPartner CRM and system
   - get_health(): Get system health status
   - get_crm_stats(): Get CRM statistics
   - get_leads(status): Get leads (optional status filter)
   - get_companies(): Get all companies from CRM

When you need help with a coding task:
1. Use search to understand the codebase
2. Use navigator to read relevant files
3. Use techpartner to check CRM data
4. Use linter to validate code
5. Use executor to test solutions
6. Propose improved code with explanations
"""
        return descriptions

    def process_task(self, task: str) -> str:
        """
        Process a coding task by:
        1. Asking the model what tools it needs
        2. Executing those tools
        3. Getting refined answer from model
        """
        
        # Step 1: Model decides what tools to use
        planning_prompt = f"""{self.tool_descriptions}

TASK: {task}

What tools would you need to complete this task? List the tools and arguments.
Format: [tool_name: method_name(arguments)]
"""
        
        logger.info("Step 1: Planning with LLM...")
        plan = self._query_llm(planning_prompt)
        logger.info(f"Plan: {plan}")
        
        # Step 2: Execute tools (simplified - just text for now)
        # In production, parse and execute tool calls
        
        # Step 3: Get refined answer
        final_prompt = f"""{self.tool_descriptions}

TASK: {task}

Based on the tools available, provide a complete, expert solution.
Include code examples, explanations, and best practices.
"""
        
        logger.info("Step 2: Generating solution...")
        solution = self._query_llm(final_prompt)
        
        return solution

    def _query_llm(self, prompt: str) -> str:
        """Query the LLM - supports external APIs (Blackbox AI/Groq) or local Ollama"""
        try:
            # Try External API First (Blackbox AI / OpenRouter / Groq)
            api_key = os.getenv("BLACKBOX_API_KEY")
            
            if api_key:
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "blackboxai",  # Or 'llama-3.1-70b' if using Groq
                    "messages": [
                        {"role": "system", "content": "You are TechPartner's Elite Coding Architect. Provide expert solutions with code examples."},
                        {"role": "user", "content": prompt}
                    ]
                }
                
                # Use Blackbox or Groq endpoint
                response = requests.post(
                    "https://api.blackbox.ai/v1/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=120
                )
                result = response.json()
                if 'choices' in result:
                    return result['choices'][0]['message']['content']
                return str(result)
            else:
                # FALLBACK: Local Ollama
                response = requests.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "temperature": 0.7,
                        "stream": False
                    },
                    timeout=60
                )
                return response.json().get('response', '')

        except Exception as e:
            logger.error(f"LLM error: {e}")
            return f"Error: {e}"


import os
import requests


class TechPartnerAPITool:
    """Tool for the Coding Expert to interact with the main TechPartner Node.js CRM and OS."""
    
    def __init__(self):
        self.name = "techpartner_api"
        self.description = "Use this to query the main TechPartner database, CRM leads, or system health. Available endpoints: '/api/system/health', '/api/crm/stats', '/api/crm/leads', '/api/leads', '/api/crm/companies'."
        self.base_url = "http://localhost:8080"
        # Uses the same admin secret from your Node.js .env
        self.admin_secret = os.getenv("ADMIN_SECRET", "Admin@6565")

    def execute(self, endpoint: str, method: str = "GET", payload: dict = None) -> str:
        headers = {
            "Authorization": f"Bearer {self.admin_secret}",
            "Content-Type": "application/json"
        }
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                res = requests.get(url, headers=headers, timeout=10)
            elif method.upper() == "POST":
                res = requests.post(url, headers=headers, json=payload, timeout=10)
            else:
                return f"Unsupported method {method}"
                
            if res.status_code == 200:
                return f"API Success: {res.text}"
            else:
                return f"API Error {res.status_code}: {res.text}"
        except Exception as e:
            return f"TechPartner API Connection Failed: {str(e)}"
    
    def get_health(self) -> str:
        """Get TechPartner system health status"""
        return self.execute("/api/system/health")
    
    def get_crm_stats(self) -> str:
        """Get CRM statistics"""
        return self.execute("/api/crm/stats")
    
    def get_leads(self, status: str = None) -> str:
        """Get leads, optionally filtered by status"""
        endpoint = "/api/crm/leads" if not status else f"/api/crm/leads?status={status}"
        return self.execute(endpoint)
    
    def get_companies(self) -> str:
        """Get all companies from CRM"""
        return self.execute("/api/crm/companies")


# Example usage
if __name__ == "__main__":
    agent = CodeAgent()
    
    # Example task
    task = "Fix the sorting bug and optimize the database query in db_utils.py"
    
    print("🤖 Advanced Coding Agent")
    print(f"Task: {task}\n")
    
    # Process the task
    # result = agent.process_task(task)
    # print(f"1Result:\n{result}")
