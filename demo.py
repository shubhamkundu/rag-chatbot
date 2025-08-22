#!/usr/bin/env python3
"""
Demo script to test the RAG chatbot functionality.
"""
import os
import sys

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import Chatbot


def test_basic_functionality():
    """Test basic chatbot functionality."""
    print("🤖 RAG Chatbot Demo")
    print("=" * 50)
    
    # Initialize chatbot
    papers_dir = os.path.join("src", "data", "papers")
    vector_store_dir = os.path.join("src", "data", "vector_store")
    
    print(f"📁 Papers directory: {papers_dir}")
    print(f"🗄️  Vector store: {vector_store_dir}")
    
    # Check if directories exist
    if not os.path.exists(papers_dir):
        os.makedirs(papers_dir, exist_ok=True)
        print(f"✅ Created papers directory: {papers_dir}")
    
    if not os.path.exists(vector_store_dir):
        os.makedirs(vector_store_dir, exist_ok=True)
        print(f"✅ Created vector store directory: {vector_store_dir}")
    
    # Initialize chatbot
    print("\n🔄 Initializing chatbot...")
    chatbot = Chatbot(
        papers_directory=papers_dir,
        vector_store_path=vector_store_dir
    )
    
    # Get status
    status = chatbot.get_status()
    print(f"\n📊 Chatbot Status:")
    print(f"  Papers found: {status['pdf_files_found']}")
    print(f"  Vector store initialized: {status['vector_store_initialized']}")
    print(f"  Ready: {status['ready']}")
    
    # Test query (will work even without papers)
    if status['pdf_files_found'] > 0:
        print(f"\n💬 Testing with {status['pdf_files_found']} papers...")
        test_query = "What are the main findings in the research papers?"
        
        print(f"Question: {test_query}")
        result = chatbot.process_query(test_query)
        print(f"Answer: {result['response']}")
        
        if result.get('source_documents'):
            print(f"Sources: {len(result['source_documents'])} documents referenced")
    else:
        print(f"\n📝 No PDF files found in {papers_dir}")
        print(f"To test with documents:")
        print(f"1. Add PDF files to {papers_dir}")
        print(f"2. Run this demo again")
        print(f"3. Or use the Streamlit/Flask interfaces to upload files")
    
    print(f"\n✅ Demo completed successfully!")
    return chatbot


def show_usage_instructions():
    """Show how to use the RAG chatbot."""
    print(f"\n🚀 How to Use the RAG Chatbot:")
    print(f"=" * 50)
    print(f"")
    print(f"1. **Streamlit Interface** (Recommended):")
    print(f"   Command: source rag-env/bin/activate && streamlit run streamlit_app.py")
    print(f"   URL: http://localhost:8501")
    print(f"   Features: File upload, chat interface, file management")
    print(f"")
    print(f"2. **Flask API**:")
    print(f"   Command: source rag-env/bin/activate && python src/app.py")
    print(f"   URL: http://localhost:5000")
    print(f"   Features: REST API, web interface, file upload")
    print(f"")
    print(f"3. **API Endpoints**:")
    print(f"   POST /ask - Ask questions")
    print(f"   POST /search - Search papers")
    print(f"   POST /upload - Upload PDF files")
    print(f"   GET /status - System status")
    print(f"")
    print(f"4. **Example API Usage**:")
    print(f'   curl -X POST http://localhost:5000/ask \\')
    print(f'     -H "Content-Type: application/json" \\')
    print(f'     -d \'{"query": "What are the main findings?"}\'')


if __name__ == "__main__":
    try:
        chatbot = test_basic_functionality()
        show_usage_instructions()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print(f"Make sure you're in the virtual environment:")
        print(f"source rag-env/bin/activate")
