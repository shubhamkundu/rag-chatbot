"""
Main chatbot class that orchestrates the RAG pipeline.
"""
import os
from typing import Dict, Any
from rag.pipeline import RAGPipeline


class Chatbot:
    def __init__(self, 
                 papers_directory: str = "data/papers",
                 vector_store_path: str = "data/vector_store"):
        """
        Initialize the RAG chatbot.
        
        Args:
            papers_directory: Directory containing research papers
            vector_store_path: Path to store/load vector database
        """
        self.papers_directory = papers_directory
        self.vector_store_path = vector_store_path
        
        # Initialize RAG pipeline
        self.rag_pipeline = RAGPipeline(vector_store_path=vector_store_path)
        
        # Load papers if directory exists and has PDF files
        self.load_papers()

    def load_papers(self):
        """Load research papers from the papers directory."""
        if not os.path.exists(self.papers_directory):
            print(f"Papers directory {self.papers_directory} does not exist.")
            print("Please create the directory and add PDF files.")
            return
        
        # Check if there are PDF files in the directory
        pdf_files = [f for f in os.listdir(self.papers_directory) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            print(f"No PDF files found in {self.papers_directory}")
            print("Please add research papers in PDF format to get started.")
            return
        
        print(f"Found {len(pdf_files)} PDF files. Loading...")
        
        # Load documents and create vector store
        self.rag_pipeline.load_documents(self.papers_directory)

    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a user query and return a structured response.
        
        Args:
            query: User's question
            
        Returns:
            Dictionary containing response and metadata
        """
        if not query or not query.strip():
            return {
                "response": "Please provide a valid question.",
                "source_documents": [],
                "error": "Empty query"
            }
        
        # Generate response using RAG pipeline
        result = self.rag_pipeline.generate_response(query.strip())
        
        return {
            "query": query,
            "response": result.get("response", "No response generated"),
            "source_documents": result.get("source_documents", []),
            "timestamp": self._get_timestamp()
        }

    def search_papers(self, query: str, k: int = 5) -> Dict[str, Any]:
        """
        Search for relevant sections in research papers.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            Dictionary containing search results
        """
        results = self.rag_pipeline.search_papers(query, k=k)
        
        return {
            "query": query,
            "results": results,
            "total_results": len(results),
            "timestamp": self._get_timestamp()
        }

    def generate_response(self, query: str) -> str:
        """
        Generate a simple text response for compatibility.
        
        Args:
            query: User's question
            
        Returns:
            Text response
        """
        result = self.process_query(query)
        return result.get("response", "Sorry, I couldn't generate a response.")

    def add_papers(self, new_papers_directory: str):
        """
        Add new papers to the existing knowledge base.
        
        Args:
            new_papers_directory: Directory containing new PDF files
        """
        if not os.path.exists(new_papers_directory):
            print(f"Directory {new_papers_directory} does not exist.")
            return
        
        self.rag_pipeline.load_documents(new_papers_directory, save_vector_store=True)
        print("New papers added successfully!")

    def get_status(self) -> Dict[str, Any]:
        """
        Get chatbot status information.
        
        Returns:
            Dictionary containing status information
        """
        has_vector_store = self.rag_pipeline.vector_store.vector_store is not None
        
        pdf_count = 0
        if os.path.exists(self.papers_directory):
            pdf_count = len([f for f in os.listdir(self.papers_directory) 
                           if f.lower().endswith('.pdf')])
        
        return {
            "papers_directory": self.papers_directory,
            "vector_store_path": self.vector_store_path,
            "pdf_files_found": pdf_count,
            "vector_store_initialized": has_vector_store,
            "ready": has_vector_store and pdf_count > 0
        }

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()