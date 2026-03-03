"""
Phase 2: Advanced RAG Pipeline
Implements semantic chunking, vector storage, and intelligent retrieval
for your entire codebase.
"""

from typing import List, Dict, Optional
from pathlib import Path
import logging
from dataclasses import dataclass
import json

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_core.callbacks import CallbackManager
from pydantic import BaseModel
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CodeChunk:
    """Represents a chunk of code with metadata"""
    content: str
    source: str
    language: str
    chunk_type: str  # "function", "class", "module", etc.
    start_line: int
    end_line: int


class SemanticCodeSplitter:
    """
    Splits code files semantically by function/class boundaries
    instead of arbitrary line counts.
    """

    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split_python_file(self, content: str, filepath: str) -> List[CodeChunk]:
        """
        Intelligently split Python files by function/class definitions.
        """
        chunks = []
        lines = content.split('\n')
        current_chunk = []
        start_line = 0

        import ast

        try:
            tree = ast.parse(content)
        except SyntaxError:
            # Fallback to character-based splitting if parsing fails
            return self._fallback_split(content, filepath)

        last_line = 0
        definitions = []

        # Extract all top-level definitions
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if hasattr(node, 'lineno'):
                    definitions.append({
                        'type': 'function' if isinstance(node, ast.FunctionDef) else 'class',
                        'name': node.name,
                        'start': node.lineno - 1,
                        'end': node.end_lineno or len(lines)
                    })

        # Create chunks around definitions
        for i, defn in enumerate(sorted(definitions, key=lambda x: x['start'])):
            chunk_text = '\n'.join(lines[defn['start']:defn['end']])
            if len(chunk_text) > 0:
                chunks.append(CodeChunk(
                    content=chunk_text,
                    source=filepath,
                    language='python',
                    chunk_type=defn['type'],
                    start_line=defn['start'],
                    end_line=defn['end']
                ))

        return chunks

    def _fallback_split(self, content: str, filepath: str) -> List[CodeChunk]:
        """Fallback to character-based splitting"""
        chunks = []
        for i in range(0, len(content), self.chunk_size - self.overlap):
            chunk = content[i:i + self.chunk_size]
            if len(chunk.strip()) > 0:
                chunks.append(CodeChunk(
                    content=chunk,
                    source=filepath,
                    language='unknown',
                    chunk_type='chunk',
                    start_line=content[:i].count('\n'),
                    end_line=content[:i + len(chunk)].count('\n')
                ))
        return chunks


class AdvancedCodeRAG:
    """
    Advanced RAG system for code with semantic search capabilities.
    """

    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        
        # Initialize embeddings (local, using Ollama)
        self.embeddings = OllamaEmbeddings(
            base_url=self.config['ollama']['base_url'],
            model=self.config['ollama']['embedding_model']
        )
        
        # Initialize vector store
        self.vector_store = None
        self.splitter = SemanticCodeSplitter(
            chunk_size=self.config['rag']['chunk_size'],
            overlap=self.config['rag']['chunk_overlap']
        )
        
        logger.info("Advanced RAG initialized with local embeddings")

    def _load_config(self, path: str) -> dict:
        """Load YAML configuration"""
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def index_directory(self, directory_path: str, file_patterns: List[str] = None):
        """
        Index an entire directory of code files into the vector store.
        
        Args:
            directory_path: Root directory to index
            file_patterns: File extensions to include (e.g., [".py", ".ts", ".js"])
        """
        if file_patterns is None:
            file_patterns = [".py", ".ts", ".js", ".java", ".go", ".cpp"]

        logger.info(f"Starting indexing of {directory_path}")
        
        all_documents = []
        directory = Path(directory_path)

        # Recursively load all matching files
        for pattern in file_patterns:
            for file_path in directory.rglob(f'*{pattern}'):
                if any(skip in str(file_path) for skip in ['.git', '__pycache__', 'node_modules', '.venv']):
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Semantic splitting for Python
                    if pattern == '.py':
                        chunks = self.splitter.split_python_file(content, str(file_path))
                    else:
                        chunks = self.splitter._fallback_split(content, str(file_path))

                    for chunk in chunks:
                        doc = Document(
                            page_content=chunk.content,
                            metadata={
                                'source': chunk.source,
                                'language': chunk.language,
                                'type': chunk.chunk_type,
                                'start_line': chunk.start_line,
                                'end_line': chunk.end_line
                            }
                        )
                        all_documents.append(doc)
                    
                    logger.info(f"Indexed {file_path}: {len(chunks)} chunks")

                except Exception as e:
                    logger.warning(f"Error indexing {file_path}: {e}")

        # Create vector store
        logger.info(f"Creating vector store with {len(all_documents)} documents...")
        self.vector_store = Chroma.from_documents(
            documents=all_documents,
            embedding=self.embeddings,
            persist_directory=self.config['rag']['chromadb_path']
        )
        self.vector_store.persist()
        logger.info("Vector store created and persisted")

    def load_vector_store(self):
        """Load existing vector store from disk"""
        if not Path(self.config['rag']['chromadb_path']).exists():
            raise ValueError("Vector store not found. Run index_directory() first.")
        
        self.vector_store = Chroma(
            embedding_function=self.embeddings,
            persist_directory=self.config['rag']['chromadb_path']
        )
        logger.info("Vector store loaded from disk")

    def search(self, query: str, k: int = 5) -> List[Dict]:
        """
        Semantic search across indexed codebase.
        
        Args:
            query: Natural language or code query
            k: Number of results to return
            
        Returns:
            List of relevant code chunks with metadata
        """
        if self.vector_store is None:
            self.load_vector_store()

        logger.info(f"Searching for: {query}")
        results = self.vector_store.similarity_search_with_score(query, k=k)

        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                'content': doc.page_content,
                'source': doc.metadata['source'],
                'language': doc.metadata['language'],
                'type': doc.metadata['type'],
                'relevance_score': score,
                'start_line': doc.metadata['start_line'],
                'end_line': doc.metadata['end_line']
            })

        return formatted_results

    def query_with_context(self, question: str, llm_client=None, k: int = 5) -> str:
        """
        Answer a question using the RAG pipeline and LLM.
        
        Args:
            question: User question
            llm_client: Ollama or other LLM client
            k: Context chunks to retrieve
            
        Returns:
            Answer from LLM with full context
        """
        # Search for relevant context
        context_chunks = self.search(question, k=k)
        
        # Format context for LLM
        context_text = "\n\n".join([
            f"[{chunk['source']}] ({chunk['type']}, lines {chunk['start_line']}-{chunk['end_line']})\n{chunk['content']}"
            for chunk in context_chunks
        ])

        # Prepare prompt
        prompt = f"""You are an advanced coding expert. Answer the following question using the provided code context.

CONTEXT FROM CODEBASE:
{context_text}

QUESTION: {question}

ANSWER:"""

        logger.info(f"RAG Context: {len(context_chunks)} chunks retrieved")
        
        return {
            'question': question,
            'context_chunks': context_chunks,
            'prompt': prompt,
            'num_chunks': len(context_chunks)
        }


# Example usage
if __name__ == "__main__":
    # Initialize RAG
    rag = AdvancedCodeRAG("config.yaml")
    
    # Index your codebase
    # rag.index_directory("/path/to/your/project")
    
    # Search
    # results = rag.search("How is database connection pooling implemented?")
    # for result in results:
    #     print(f"\n{result['source']}:\n{result['content']}\n")
