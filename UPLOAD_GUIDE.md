# File Upload Functionality Documentation

## Overview
Your RAG chatbot now supports file upload functionality through both the Streamlit and Flask interfaces.

## New Features Added:

### 1. Streamlit Interface Enhancements:
- **File Upload Widget**: Upload multiple PDF files simultaneously
- **File Management**: View, delete, and manage uploaded documents
- **Real-time Processing**: Automatic chatbot reload after successful uploads
- **File Validation**: Only accepts PDF files

### 2. Flask API Enhancements:
- **Upload Endpoint**: `POST /upload` for programmatic file uploads
- **Enhanced Web Interface**: File upload directly in the web UI
- **File Validation**: Server-side PDF validation
- **Progress Feedback**: Real-time upload status and results

## Usage Instructions:

### Streamlit Interface:
1. Run the app: `streamlit run streamlit_app.py`
2. Navigate to the "File Management" section in the sidebar
3. Use the "Upload Documents" section to select and upload PDF files
4. Click "Save Uploaded Files" to process and add them to the knowledge base
5. Start chatting with your documents!

### Flask Interface:
1. Run the app: `python src/app.py`
2. Open http://localhost:5000 in your browser
3. Use the file upload section at the top of the page
4. Select PDF files and click "Upload Files"
5. The system will automatically process and reload the chatbot

### API Usage:
```bash
# Upload files via API
curl -X POST http://localhost:5000/upload \
  -F "files=@document1.pdf" \
  -F "files=@document2.pdf"
```

## File Processing Flow:
1. **Upload**: Files are uploaded to the UI
2. **Validation**: System checks for PDF format
3. **Storage**: Files are saved to `src/data/papers/` directory
4. **Processing**: Documents are loaded and chunked
5. **Embedding**: Text chunks are converted to vector embeddings
6. **Storage**: Embeddings are stored in FAISS vector database
7. **Ready**: Chatbot is ready to answer questions about the uploaded documents

## Key Components:

### Enhanced Streamlit App (`streamlit_app.py`):
- File uploader widget with multiple file support
- File management with delete functionality
- Real-time status updates
- Error handling and user feedback

### Enhanced Flask App (`src/app.py`):
- `/upload` endpoint for file uploads
- Secure filename handling
- File validation and error handling
- Automatic chatbot reloading

### Core Processing (`src/chatbot/__init__.py`):
- Document loading and processing
- Vector store management
- Query processing with uploaded documents

## Security Features:
- File type validation (PDF only)
- Secure filename handling to prevent path injection
- File size limits (50MB max per upload)
- Error handling for malformed files

## Error Handling:
- Invalid file types are rejected
- Corrupted PDF files are handled gracefully
- Upload failures are reported with specific error messages
- Partial uploads are supported (some files can succeed while others fail)

## Next Steps:
1. Upload some PDF research papers
2. Start asking questions about the content
3. Use the search functionality to find specific information
4. Explore the different interfaces (Streamlit vs Flask)

Your RAG chatbot is now fully functional with file upload capabilities!
