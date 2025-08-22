"""
FAISS vector store implementation for document embeddings.
"""
import os
from typing import List, Optional
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document


class FAISSVectorStore:
    """
    FAISS-based vector store for efficient similarity search.
    
    Handles document embeddings, storage, and retrieval using FAISS.
    """
    
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the FAISS vector store.
        
        Args:
            model_name (str): HuggingFace model name for embeddings
        """
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'}
        )
        self.vector_store: Optional[FAISS] = None
        self.store_path: Optional[str] = None
        
    def load_vector_store(self, store_path):
        """
        Load existing vector store from disk.
        
        Args:
            store_path (str): Path to the vector store directory
        """
        # Check if the actual FAISS index file exists
        index_file = os.path.join(store_path, "index.faiss")
        if not os.path.exists(index_file):
            print(f"Vector store index not found at {index_file}. Will be created when documents are added.")
            return False
        
        try:
            self.vector_store = FAISS.load_local(
                store_path, 
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            self.store_path = store_path
            print(f"Vector store loaded from {store_path}")
            return True
        except Exception as e:
            print(f"Failed to load vector store: {e}")
            return False

    def create_vector_store(self, documents: List[Document], store_path: Optional[str] = None):
        """
        Create a new vector store from documents.
        
        Args:
            documents (List[Document]): List of documents to embed
            store_path (str, optional): Path to save the vector store
        """
        if not documents:
            raise ValueError("No documents provided to create vector store")
        
        print(f"Creating vector store from {len(documents)} documents...")
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        
        if store_path:
            self.save_vector_store(store_path)
            
        print(f"Vector store created successfully")
        
    def add_documents(self, documents: List[Document]):
        """
        Add new documents to existing vector store.
        
        Args:
            documents (List[Document]): List of new documents to add
        """
        if not documents:
            print("No documents to add")
            return
            
        if self.vector_store is None:
            print("No existing vector store found. Creating new one...")
            self.create_vector_store(documents)
        else:
            print(f"Adding {len(documents)} documents to existing vector store...")
            self.vector_store.add_documents(documents)
            
        # Save if we have a store path
        if self.store_path:
            self.save_vector_store(self.store_path)
            
    def save_vector_store(self, store_path: str):
        """
        Save the vector store to disk.
        
        Args:
            store_path (str): Path to save the vector store
        """
        if self.vector_store is None:
            raise ValueError("No vector store to save")
            
        # Ensure directory exists
        os.makedirs(os.path.dirname(store_path), exist_ok=True)
        
        self.vector_store.save_local(store_path)
        self.store_path = store_path
        print(f"Vector store saved to {store_path}")
        
    def delete_vector_store(self, store_path: str):
        """
        Delete vector store from disk.
        
        Args:
            store_path (str): Path to the vector store directory
        """
        if not os.path.exists(store_path):
            print(f"Vector store path {store_path} does not exist")
            return
            
        # Remove all files in the directory
        import shutil
        shutil.rmtree(store_path)
        print(f"Vector store deleted from {store_path}")
        
    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """
        Perform similarity search on the vector store.
        
        Args:
            query (str): Search query
            k (int): Number of similar documents to return
            
        Returns:
            List[Document]: List of similar documents
        """
        if self.vector_store is None:
            print("No vector store available for search")
            return []
            
        try:
            results = self.vector_store.similarity_search(query, k=k)
            return results
        except Exception as e:
            print(f"Error during similarity search: {e}")
            return []
            
    def similarity_search_with_score(self, query: str, k: int = 5) -> List[tuple]:
        """
        Perform similarity search with relevance scores.
        
        Args:
            query (str): Search query
            k (int): Number of similar documents to return
            
        Returns:
            List[tuple]: List of (document, score) tuples
        """
        if self.vector_store is None:
            print("No vector store available for search")
            return []
            
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            return results
        except Exception as e:
            print(f"Error during similarity search with scores: {e}")
            return []
            
    def get_retriever(self, search_kwargs: Optional[dict] = None):
        """
        Get a retriever object for the vector store.
        
        Args:
            search_kwargs (dict, optional): Search parameters
            
        Returns:
            VectorStoreRetriever: Retriever object
        """
        if self.vector_store is None:
            raise ValueError("No vector store available to create retriever")
            
        search_kwargs = search_kwargs or {"k": 5}
        return self.vector_store.as_retriever(search_kwargs=search_kwargs)
        
    def is_initialized(self) -> bool:
        """
        Check if the vector store is initialized.
        
        Returns:
            bool: True if vector store is ready, False otherwise
        """
        return self.vector_store is not None
        
    def get_document_count(self) -> int:
        """
        Get the number of documents in the vector store.
        
        Returns:
            int: Number of documents
        """
        if self.vector_store is None:
            return 0
        try:
            return self.vector_store.index.ntotal
        except:
            return 0
