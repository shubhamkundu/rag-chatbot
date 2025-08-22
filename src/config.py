"""
Configuration settings for the RAG chatbot.
"""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class ModelConfig:
    """Configuration for AI models."""
    embedding_model: str = "all-MiniLM-L6-v2"  # Sentence transformer model
    llm_model: str = "microsoft/DialoGPT-small"  # Language model
    max_new_tokens: int = 200
    temperature: float = 0.7
    device: str = "cpu"  # Use "cuda" if GPU available


@dataclass
class VectorStoreConfig:
    """Configuration for vector store."""
    chunk_size: int = 1000
    chunk_overlap: int = 200
    similarity_k: int = 5  # Number of similar documents to retrieve
    store_path: str = "src/data/vector_store"


@dataclass
class DataConfig:
    """Configuration for data handling."""
    papers_directory: str = "src/data/papers"
    supported_formats: list = None
    
    def __post_init__(self):
        if self.supported_formats is None:
            self.supported_formats = [".pdf"]


@dataclass
class AppConfig:
    """Configuration for the application."""
    flask_host: str = "0.0.0.0"
    flask_port: int = 5000
    flask_debug: bool = True
    streamlit_port: int = 8501
    
    # UI Settings
    max_chat_history: int = 50
    response_timeout: int = 30  # seconds


class Config:
    """Main configuration class."""
    
    def __init__(self, config_file: Optional[str] = None):
        self.model = ModelConfig()
        self.vector_store = VectorStoreConfig()
        self.data = DataConfig()
        self.app = AppConfig()
        
        # Load from environment variables if available
        self._load_from_env()
        
        # Load from config file if provided
        if config_file and os.path.exists(config_file):
            self._load_from_file(config_file)
    
    def _load_from_env(self):
        """Load configuration from environment variables."""
        # Model settings
        if os.getenv("EMBEDDING_MODEL"):
            self.model.embedding_model = os.getenv("EMBEDDING_MODEL")
        
        if os.getenv("LLM_MODEL"):
            self.model.llm_model = os.getenv("LLM_MODEL")
        
        if os.getenv("DEVICE"):
            self.model.device = os.getenv("DEVICE")
        
        # Paths
        if os.getenv("PAPERS_DIRECTORY"):
            self.data.papers_directory = os.getenv("PAPERS_DIRECTORY")
        
        if os.getenv("VECTOR_STORE_PATH"):
            self.vector_store.store_path = os.getenv("VECTOR_STORE_PATH")
        
        # App settings
        if os.getenv("FLASK_PORT"):
            self.app.flask_port = int(os.getenv("FLASK_PORT"))
        
        if os.getenv("FLASK_DEBUG"):
            self.app.flask_debug = os.getenv("FLASK_DEBUG").lower() == "true"
    
    def _load_from_file(self, config_file: str):
        """Load configuration from file (future implementation)."""
        # Could implement JSON/YAML config file loading here
        pass
    
    def create_directories(self):
        """Create necessary directories."""
        directories = [
            self.data.papers_directory,
            self.vector_store.store_path,
            os.path.dirname(self.vector_store.store_path)
        ]
        
        for directory in directories:
            if directory:
                os.makedirs(directory, exist_ok=True)
    
    def validate(self) -> bool:
        """Validate configuration."""
        # Check if required directories can be created
        try:
            self.create_directories()
        except Exception as e:
            print(f"Error creating directories: {e}")
            return False
        
        return True
    
    def get_papers_count(self) -> int:
        """Get number of PDF files in papers directory."""
        if not os.path.exists(self.data.papers_directory):
            return 0
        
        pdf_files = [
            f for f in os.listdir(self.data.papers_directory)
            if any(f.lower().endswith(ext) for ext in self.data.supported_formats)
        ]
        
        return len(pdf_files)
    
    def print_config(self):
        """Print current configuration."""
        print("🔧 Current Configuration:")
        print(f"  📁 Papers Directory: {self.data.papers_directory}")
        print(f"  🗄️  Vector Store: {self.vector_store.store_path}")
        print(f"  🤖 Embedding Model: {self.model.embedding_model}")
        print(f"  💬 Language Model: {self.model.llm_model}")
        print(f"  🖥️  Device: {self.model.device}")
        print(f"  🌐 Flask Port: {self.app.flask_port}")
        print(f"  📄 PDF Files Found: {self.get_papers_count()}")


# Global configuration instance
config = Config()

# Environment-specific configurations
DEVELOPMENT_CONFIG = {
    "flask_debug": True,
    "llm_model": "microsoft/DialoGPT-small",  # Smaller model for development
    "max_new_tokens": 100
}

PRODUCTION_CONFIG = {
    "flask_debug": False,
    "llm_model": "microsoft/DialoGPT-medium",  # Better model for production
    "max_new_tokens": 200
}
