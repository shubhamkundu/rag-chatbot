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
            return Falsemport List, Optional
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


class FAISSVectorStore:
    def __init__(self, embedding_model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the FAISS vector store.
        
        Args:
            embedding_model_name: Name of the HuggingFace embedding model
        """
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model_name,
            model_kwargs={'device': 'cpu'}
        )
        self.vector_store: Optional[FAISS] = None
        self.store_path = None

    def create_vector_store(self, documents: List[Document], store_path: Optional[str] = None):
        """
        Create a FAISS vector store from documents.
        
        Args:
            documents: List of Document objects
            store_path: Path to save the vector store (optional)
        """
        if not documents:
            raise ValueError("No documents provided to create vector store")
        
        # Create FAISS vector store from documents
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        
        # Save vector store if path is provided
        if store_path:
            self.save_vector_store(store_path)
            
        print(f"Created vector store with {len(documents)} documents")

    def add_documents(self, documents: List[Document]):
        """
        Add new documents to existing vector store.
        
        Args:
            documents: List of Document objects to add
        """
        if self.vector_store is None:
            raise ValueError("Vector store not initialized. Create vector store first.")
        
        self.vector_store.add_documents(documents)
        print(f"Added {len(documents)} documents to vector store")

    def save_vector_store(self, store_path: str):
        """
        Save the vector store to disk.
        
        Args:
            store_path: Path to save the vector store
        """
        if self.vector_store is None:
            raise ValueError("No vector store to save")
        
        os.makedirs(os.path.dirname(store_path), exist_ok=True)
        self.vector_store.save_local(store_path)
        self.store_path = store_path
        print(f"Vector store saved to {store_path}")

    def load_vector_store(self, store_path: str):
        """
        Load vector store from disk.
        
        Args:
            store_path: Path to load the vector store from
        """
        if not os.path.exists(store_path):
            raise FileNotFoundError(f"Vector store not found at {store_path}")
        
        self.vector_store = FAISS.load_local(
            store_path, 
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        self.store_path = store_path
        print(f"Vector store loaded from {store_path}")

    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """
        Perform similarity search on the vector store.
        
        Args:
            query: Search query
            k: Number of similar documents to return
            
        Returns:
            List of similar documents
        """
        if self.vector_store is None:
            raise ValueError("Vector store not initialized")
        
        return self.vector_store.similarity_search(query, k=k)

    def similarity_search_with_score(self, query: str, k: int = 5) -> List[tuple]:
        """
        Perform similarity search with scores.
        
        Args:
            query: Search query
            k: Number of similar documents to return
            
        Returns:
            List of tuples (document, score)
        """
        if self.vector_store is None:
            raise ValueError("Vector store not initialized")
        
        return self.vector_store.similarity_search_with_score(query, k=k)

    def get_retriever(self, search_kwargs: Optional[dict] = None):
        """
        Get a retriever object for use with chains.
        
        Args:
            search_kwargs: Additional search parameters
            
        Returns:
            Retriever object
        """
        if self.vector_store is None:
            raise ValueError("Vector store not initialized")
        
        if search_kwargs is None:
            search_kwargs = {"k": 5}
            
        return self.vector_store.as_retriever(search_kwargs=search_kwargs)