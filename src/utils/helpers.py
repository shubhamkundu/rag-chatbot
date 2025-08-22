"""
Utility functions for the RAG chatbot.
"""
import re
import os
from typing import List, Dict, Any


def preprocess_text(text: str) -> str:
    """
    Preprocess text for better processing.
    
    Args:
        text: Raw text to preprocess
        
    Returns:
        Preprocessed text
    """
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters that might interfere
    text = text.replace('\x00', '')
    text = text.replace('\n', ' ')
    text = text.replace('\t', ' ')
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def format_response(response: str, sources: List[str] = None) -> str:
    """
    Format the chatbot's response for display.
    
    Args:
        response: The generated response
        sources: List of source documents (optional)
        
    Returns:
        Formatted response string
    """
    formatted = f"🤖 **Answer:** {response}"
    
    if sources:
        formatted += f"\n\n📚 **Sources:**"
        for i, source in enumerate(sources, 1):
            # Truncate source if too long
            source_preview = source[:100] + "..." if len(source) > 100 else source
            formatted += f"\n{i}. {source_preview}"
    
    return formatted


def validate_pdf_file(file_path: str) -> bool:
    """
    Validate if a file is a valid PDF.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if valid PDF, False otherwise
    """
    if not os.path.exists(file_path):
        return False
    
    if not file_path.lower().endswith('.pdf'):
        return False
    
    try:
        # Basic PDF validation - check file starts with PDF header
        with open(file_path, 'rb') as f:
            header = f.read(4)
            return header == b'%PDF'
    except Exception:
        return False


def create_directory_if_not_exists(directory_path: str):
    """
    Create directory if it doesn't exist.
    
    Args:
        directory_path: Path to the directory
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)
        print(f"Created directory: {directory_path}")


def get_file_info(file_path: str) -> Dict[str, Any]:
    """
    Get information about a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Dictionary containing file information
    """
    if not os.path.exists(file_path):
        return {"exists": False}
    
    stat = os.stat(file_path)
    
    return {
        "exists": True,
        "name": os.path.basename(file_path),
        "size": stat.st_size,
        "size_mb": round(stat.st_size / (1024 * 1024), 2),
        "modified": stat.st_mtime,
        "is_pdf": file_path.lower().endswith('.pdf')
    }


def truncate_text(text: str, max_length: int = 500) -> str:
    """
    Truncate text to specified length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length] + "..."


def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extract keywords from text (simple implementation).
    
    Args:
        text: Input text
        max_keywords: Maximum number of keywords to return
        
    Returns:
        List of keywords
    """
    # Simple keyword extraction - remove common words and get frequent terms
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must', 'this', 'that', 'these', 'those'}
    
    # Extract words (simple tokenization)
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Filter out stop words
    keywords = [word for word in words if word not in stop_words]
    
    # Get unique keywords and return top ones
    unique_keywords = list(set(keywords))
    
    return unique_keywords[:max_keywords]