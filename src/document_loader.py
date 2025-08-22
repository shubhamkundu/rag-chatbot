"""
Document loader for processing research papers (PDF files).
"""
import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class DocumentLoader:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the document loader.
        
        Args:
            chunk_size: Size of each text chunk
            chunk_overlap: Overlap between consecutive chunks
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_pdf(self, file_path: str) -> List[Document]:
        """
        Load a single PDF file and split it into chunks.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of Document objects
        """
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        # Split documents into chunks
        chunks = self.text_splitter.split_documents(documents)
        
        # Add metadata
        for chunk in chunks:
            chunk.metadata['source'] = os.path.basename(file_path)
            
        return chunks
    
    def load_papers_from_directory(self, directory_path: str) -> List[Document]:
        """
        Load all PDF files from a directory.
        
        Args:
            directory_path: Path to directory containing PDF files
            
        Returns:
            List of all document chunks
        """
        all_chunks = []
        
        for filename in os.listdir(directory_path):
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(directory_path, filename)
                try:
                    chunks = self.load_pdf(file_path)
                    all_chunks.extend(chunks)
                    print(f"Loaded {len(chunks)} chunks from {filename}")
                except Exception as e:
                    print(f"Error loading {filename}: {str(e)}")
        
        return all_chunks
    
    def preprocess_text(self, text: str) -> str:
        """
        Basic text preprocessing.
        
        Args:
            text: Raw text to preprocess
            
        Returns:
            Preprocessed text
        """
        # Remove excessive whitespace
        text = " ".join(text.split())
        
        # Remove special characters that might interfere with processing
        text = text.replace('\x00', '')
        
        return text
