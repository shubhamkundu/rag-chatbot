# Research Paper RAG Chatbot 🤖📚

A sophisticated chatbot that uses **Retrieval-Augmented Generation (RAG)** to answer questions about your research papers. Built with LangChain, FAISS vector database, HuggingFace transformers, and provides both Flask API and Streamlit web interfaces.

## Features ✨

- 🔍 **Semantic Search**: Find relevant content across multiple research papers
- 🤖 **AI-Powered Responses**: Generate contextual answers using state-of-the-art language models
- 📄 **PDF Processing**: Automatically extract and chunk text from PDF research papers
- � **File Upload**: Upload PDF files directly through the web interface
- �🗄️ **Vector Database**: Efficient similarity search using FAISS
- 🌐 **Dual Interface**: Both REST API (Flask) and Web UI (Streamlit)
- 💾 **Persistent Storage**: Save and load vector embeddings for quick startup
- 🔧 **Configurable**: Easily customize models, chunk sizes, and other parameters

## Quick Start 🚀

### 1. Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd rag-chatbot

# Run setup script (creates directories and installs dependencies)
python setup.py
```

### 2. Add Research Papers

**Option A: Upload via Web Interface (Recommended)**
- Run the Streamlit app: `streamlit run streamlit_app.py`
- Use the file upload section in the sidebar to upload PDF files
- Or run the Flask app: `python src/app.py` and upload files at http://localhost:5000

**Option B: Manual File Placement**
```bash
# Add your PDF research papers to the papers directory
cp your-research-papers/*.pdf src/data/papers/
```

### 3. Run the Application

**Option A: Streamlit Web Interface (Recommended)**
```bash
streamlit run streamlit_app.py
```
Then open http://localhost:8501

**Option B: Flask API**
```bash
python src/app.py
```
Then open http://localhost:5000

## Project Structure 📁

```
rag-chatbot/
├── src/
│   ├── app.py                 # Flask API application
│   ├── config.py              # Configuration settings
│   ├── document_loader.py     # PDF processing and text chunking
│   ├── chatbot/
│   │   └── __init__.py        # Main chatbot orchestration
│   ├── data/
│   │   ├── papers/            # 📄 Place your PDF papers here
│   │   └── vector_store/      # 🗄️ Auto-generated vector database
│   ├── rag/
│   │   └── pipeline.py        # RAG implementation
│   ├── vectorstore/
│   │   └── faiss_store.py     # FAISS vector store wrapper
│   └── utils/
│       └── helpers.py         # Utility functions
├── streamlit_app.py           # Streamlit web interface
├── setup.py                   # Setup and installation script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## API Endpoints 🌐

### Flask API (http://localhost:5000)

| Endpoint | Method | Description | Body |
|----------|--------|-------------|------|
| `/` | GET | Web interface | - |
| `/ask` | POST | Ask a question | `{"query": "your question"}` |
| `/search` | POST | Search papers | `{"query": "search terms", "k": 5}` |
| `/upload` | POST | Upload PDF files | Form data with `files` field |
| `/status` | GET | System status | - |
| `/reload` | POST | Reload papers | - |

### Example API Usage

```bash
# Ask a question
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the main findings about machine learning?"}'

# Search papers
curl -X POST http://localhost:5000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "neural networks", "k": 3}'

# Upload files
curl -X POST http://localhost:5000/upload \
  -F "files=@research_paper1.pdf" \
  -F "files=@research_paper2.pdf"

# Check status
curl http://localhost:5000/status
```

## Configuration ⚙️

### Environment Variables

```bash
# Model settings
export EMBEDDING_MODEL="all-MiniLM-L6-v2"
export LLM_MODEL="microsoft/DialoGPT-small"
export DEVICE="cpu"  # or "cuda" for GPU

# Paths
export PAPERS_DIRECTORY="src/data/papers"
export VECTOR_STORE_PATH="src/data/vector_store"

# App settings
export FLASK_PORT="5000"
export FLASK_DEBUG="true"
```

### Model Configuration

Edit `src/config.py` to customize:

- **Embedding Model**: Choose from HuggingFace sentence transformers
- **Language Model**: Select from HuggingFace transformers
- **Chunk Size**: Adjust text chunking parameters
- **Similarity Threshold**: Fine-tune retrieval sensitivity

## Supported Models 🤖

### Embedding Models (Recommended)
- `all-MiniLM-L6-v2` (default) - Good balance of speed and quality
- `all-mpnet-base-v2` - Higher quality, slower
- `all-distilroberta-v1` - Fast and efficient

### Language Models
- `microsoft/DialoGPT-small` (default) - Fast, good for development
- `microsoft/DialoGPT-medium` - Better quality
- `facebook/blenderbot-small-90M` - Conversation-focused
- Any HuggingFace causal LM model

## Usage Examples 💡

### Questions You Can Ask

- **Summarization**: "What are the main conclusions of the papers?"
- **Specific Findings**: "What did the study find about neural network accuracy?"
- **Methodology**: "What datasets were used in the research?"
- **Comparisons**: "How do the different approaches compare?"
- **Technical Details**: "What hyperparameters were used for training?"

### Streamlit Interface Features

- 💬 **Interactive Chat**: Real-time conversation interface
- 🔍 **Quick Search**: Find relevant paper sections
- 📊 **System Status**: Monitor papers loaded and system health
- 📁 **File Management**: View loaded papers and their status
- 🔄 **Hot Reload**: Refresh papers without restarting

## Installation Details 📦

### Dependencies

- **LangChain**: RAG framework and document processing
- **FAISS**: Vector similarity search
- **HuggingFace Transformers**: Language and embedding models
- **Sentence Transformers**: Text embeddings
- **PyPDF**: PDF text extraction
- **Streamlit**: Web interface
- **Flask**: REST API

### Manual Installation

```bash
# Create virtual environment (recommended)
python -m venv rag-env
source rag-env/bin/activate  # On Windows: rag-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir -p src/data/papers
mkdir -p src/data/vector_store
```

## Troubleshooting 🔧

### Common Issues

**"No PDF files found"**
- Ensure PDF files are in `src/data/papers/`
- Check file extensions (must be `.pdf`)
- Verify files are readable (not corrupted)

**"Vector store not initialized"**
- Add PDF files first
- Run `/reload` endpoint or restart application
- Check paper directory permissions

**"Import errors"**
- Run `pip install -r requirements.txt`
- Check Python version (3.8+ recommended)
- Try creating a new virtual environment

**"Model loading errors"**
- Check internet connection (models download on first use)
- Verify disk space for model cache
- Try smaller models if memory is limited

### Performance Tips

- **GPU Acceleration**: Set `DEVICE="cuda"` if you have a compatible GPU
- **Model Selection**: Use smaller models for faster responses
- **Chunk Size**: Adjust based on paper length and detail needed
- **Vector Store**: Reuse saved vector stores to avoid reprocessing

## Development 👨‍💻

### Adding New Features

1. **Custom Models**: Modify `src/config.py` and `src/rag/pipeline.py`
2. **New File Types**: Extend `src/document_loader.py`
3. **API Endpoints**: Add routes in `src/app.py`
4. **UI Components**: Enhance `streamlit_app.py`

### Testing

```bash
# Test with sample papers
python setup.py

# Add test PDFs to src/data/papers/
# Run the application and test queries
```

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- **LangChain** for the RAG framework
- **HuggingFace** for transformer models
- **Facebook Research** for FAISS
- **Streamlit** for the web interface

---

**Built with ❤️ for researchers and academics**

Need help? Open an issue or check the troubleshooting section above!

## Overview of Functionality

- **Retrieval-Augmented Generation (RAG)**: Combines retrieval of documents with generative capabilities to provide accurate and contextually relevant answers.
- **FAISS Vector Store**: Efficiently manages and queries embeddings of research papers for fast retrieval.
- **Langchain and Hugging Face**: Utilized for building the language model and handling natural language processing tasks.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.