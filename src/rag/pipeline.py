"""
RAG (Retrieval-Augmented Generation) pipeline implementation.
"""
import os
from typing import List, Optional
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

from vectorstore.faiss_store import FAISSVectorStore
from document_loader import DocumentLoader


class RAGPipeline:
    def __init__(self, 
                 model_name: str = "microsoft/DialoGPT-medium",
                 embedding_model: str = "all-MiniLM-L6-v2",
                 vector_store_path: str = None):
        """
        Initialize the RAG pipeline.
        
        Args:
            model_name: Name of the language model
            embedding_model: Name of the embedding model
            vector_store_path: Path to existing vector store (optional)
        """
        self.model_name = model_name
        self.embedding_model = embedding_model
        self.vector_store_path = vector_store_path
        
        # Initialize components
        self.vector_store = FAISSVectorStore(embedding_model)
        self.document_loader = DocumentLoader()
        self.llm = None
        self.qa_chain = None
        
        # Load vector store if path provided
        if vector_store_path and os.path.exists(vector_store_path):
            self.vector_store.load_vector_store(vector_store_path)
        
        # Initialize the language model
        self._initialize_llm()
        
        # Setup QA chain
        self._setup_qa_chain()

    def _initialize_llm(self):
        """Initialize the language model pipeline."""
        try:
            # Use a smaller, more efficient model for CPU usage
            model_name = "microsoft/DialoGPT-small"  # Smaller model for better performance
            
            # Create text generation pipeline
            text_generation_pipeline = pipeline(
                "text-generation",
                model=model_name,
                tokenizer=model_name,
                max_new_tokens=200,
                temperature=0.7,
                do_sample=True,
                device=-1  # Use CPU
            )
            
            self.llm = HuggingFacePipeline(pipeline=text_generation_pipeline)
            print(f"Initialized language model: {model_name}")
            
        except Exception as e:
            print(f"Error initializing language model: {e}")
            # Fallback to a simple response generator
            self.llm = None

    def _setup_qa_chain(self):
        """Setup the question-answering chain."""
        if self.vector_store.vector_store is None:
            print("Vector store not available. QA chain not initialized.")
            return
        
        # Define prompt template
        prompt_template = """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.

        Context: {context}

        Question: {question}
        Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template, 
            input_variables=["context", "question"]
        )
        
        # Create retriever
        retriever = self.vector_store.get_retriever(search_kwargs={"k": 3})
        
        # Create QA chain
        if self.llm:
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=retriever,
                chain_type_kwargs={"prompt": PROMPT},
                return_source_documents=True
            )
        
        print("QA chain initialized successfully")

    def load_documents(self, papers_directory: str, save_vector_store: bool = True):
        """
        Load research papers and create/update vector store.
        
        Args:
            papers_directory: Directory containing PDF papers
            save_vector_store: Whether to save the vector store to disk
        """
        print(f"Loading documents from {papers_directory}")
        
        # Load documents
        documents = self.document_loader.load_papers_from_directory(papers_directory)
        
        if not documents:
            print("No documents found in the specified directory")
            return
        
        # Create or update vector store
        if self.vector_store.vector_store is None:
            store_path = self.vector_store_path or "data/vector_store"
            self.vector_store.create_vector_store(documents, store_path if save_vector_store else None)
        else:
            self.vector_store.add_documents(documents)
            if save_vector_store and self.vector_store_path:
                self.vector_store.save_vector_store(self.vector_store_path)
        
        # Reinitialize QA chain with new vector store
        self._setup_qa_chain()

    def generate_response(self, query: str) -> dict:
        """
        Generate response for a user query.
        
        Args:
            query: User question
            
        Returns:
            Dictionary containing response and source documents
        """
        if self.vector_store.vector_store is None:
            return {
                "response": "Vector store not initialized. Please load documents first.",
                "source_documents": []
            }
        
        try:
            # If we have a QA chain, use it
            if self.qa_chain:
                result = self.qa_chain({"query": query})
                return {
                    "response": result["result"],
                    "source_documents": [doc.page_content[:200] + "..." for doc in result.get("source_documents", [])]
                }
            else:
                # Fallback: simple retrieval without generation
                docs = self.vector_store.similarity_search(query, k=3)
                context = "\n\n".join([doc.page_content for doc in docs])
                
                # Simple template-based response
                response = f"Based on the research papers, here are the relevant findings:\n\n{context[:500]}..."
                
                return {
                    "response": response,
                    "source_documents": [doc.page_content[:200] + "..." for doc in docs]
                }
                
        except Exception as e:
            print(f"Error generating response: {e}")
            return {
                "response": f"Sorry, I encountered an error while processing your query: {str(e)}",
                "source_documents": []
            }

    def search_papers(self, query: str, k: int = 5) -> List[dict]:
        """
        Search for relevant paper sections.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of relevant document sections with metadata
        """
        if self.vector_store.vector_store is None:
            return []
        
        try:
            docs_with_scores = self.vector_store.similarity_search_with_score(query, k=k)
            
            results = []
            for doc, score in docs_with_scores:
                results.append({
                    "content": doc.page_content,
                    "source": doc.metadata.get("source", "Unknown"),
                    "page": doc.metadata.get("page", "Unknown"),
                    "similarity_score": float(score)
                })
            
            return results
            
        except Exception as e:
            print(f"Error searching papers: {e}")
            return []