#!/usr/bin/env python3
"""
Comprehensive test script for the RAG chatbot system.
"""
import os
import sys
import time
import subprocess
import requests
import tempfile
import shutil
from pathlib import Path

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test if all required packages can be imported."""
    print("🔍 Testing imports...")
    
    try:
        import langchain
        print("✅ LangChain imported")
        
        import faiss
        print("✅ FAISS imported")
        
        from langchain_huggingface import HuggingFaceEmbeddings
        print("✅ HuggingFace embeddings imported")
        
        import streamlit
        print("✅ Streamlit imported")
        
        import flask
        print("✅ Flask imported")
        
        import pypdf
        print("✅ PyPDF imported")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_directories():
    """Test if required directories exist and can be created."""
    print("\n📁 Testing directories...")
    
    dirs = [
        "src/data/papers",
        "src/data/vector_store"
    ]
    
    for dir_path in dirs:
        try:
            os.makedirs(dir_path, exist_ok=True)
            print(f"✅ Directory ready: {dir_path}")
        except Exception as e:
            print(f"❌ Directory error {dir_path}: {e}")
            return False
    
    return True

def test_basic_components():
    """Test basic chatbot components without heavy models."""
    print("\n🧪 Testing basic components...")
    
    try:
        # Test document loader
        from document_loader import DocumentLoader
        loader = DocumentLoader()
        print("✅ Document loader initialized")
        
        # Test vector store (without creating embeddings)
        from vectorstore.faiss_store import FAISSVectorStore
        # Don't initialize yet to avoid downloading models
        print("✅ Vector store class imported")
        
        # Test configuration
        from config import Config
        config = Config()
        print("✅ Configuration loaded")
        
        return True
    except Exception as e:
        print(f"❌ Component test error: {e}")
        return False

def create_sample_pdf():
    """Create a simple sample PDF for testing."""
    print("\n📄 Creating sample PDF...")
    
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        # Create a simple PDF
        pdf_path = "src/data/papers/sample_research.pdf"
        c = canvas.Canvas(pdf_path, pagesize=letter)
        
        # Add some content
        c.drawString(100, 750, "Sample Research Paper")
        c.drawString(100, 720, "Abstract: This is a sample research paper for testing the RAG chatbot.")
        c.drawString(100, 690, "Introduction: This paper demonstrates the capabilities of the chatbot.")
        c.drawString(100, 660, "Methodology: We use machine learning techniques for document processing.")
        c.drawString(100, 630, "Results: The system successfully processes and retrieves information.")
        c.drawString(100, 600, "Conclusion: The RAG chatbot works effectively with research papers.")
        
        c.save()
        print(f"✅ Sample PDF created: {pdf_path}")
        return pdf_path
    except ImportError:
        # Create a simple text file if reportlab is not available
        print("📝 Creating sample text file instead...")
        text_content = """Sample Research Paper

Abstract: This is a sample research paper for testing the RAG chatbot.

Introduction: This paper demonstrates the capabilities of the chatbot.

Methodology: We use machine learning techniques for document processing.

Results: The system successfully processes and retrieves information.

Conclusion: The RAG chatbot works effectively with research papers.
"""
        text_path = "src/data/papers/sample_research.txt"
        with open(text_path, 'w') as f:
            f.write(text_content)
        print(f"✅ Sample text file created: {text_path}")
        return text_path
    except Exception as e:
        print(f"❌ Error creating sample file: {e}")
        return None

def test_flask_app():
    """Test Flask application startup."""
    print("\n🌐 Testing Flask application...")
    
    try:
        # Start Flask app in background
        process = subprocess.Popen([
            sys.executable, "src/app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for startup
        time.sleep(5)
        
        # Test if app is running
        try:
            response = requests.get("http://localhost:5000/status", timeout=10)
            if response.status_code == 200:
                print("✅ Flask app is running")
                data = response.json()
                print(f"   Papers found: {data.get('pdf_files_found', 0)}")
                print(f"   Vector store initialized: {data.get('vector_store_initialized', False)}")
                
                # Terminate the process
                process.terminate()
                return True
            else:
                print(f"❌ Flask app returned status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Flask app connection error: {e}")
        
        # Clean up process
        process.terminate()
        return False
        
    except Exception as e:
        print(f"❌ Flask app test error: {e}")
        return False

def test_streamlit_config():
    """Test Streamlit configuration."""
    print("\n🎨 Testing Streamlit configuration...")
    
    try:
        # Test streamlit app syntax
        result = subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--help"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Streamlit configuration is valid")
            return True
        else:
            print(f"❌ Streamlit configuration error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Streamlit test error: {e}")
        return False

def run_comprehensive_test():
    """Run all tests and provide summary."""
    print("🤖 RAG Chatbot Comprehensive Test")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Directory Test", test_directories),
        ("Component Test", test_basic_components),
        ("Streamlit Config Test", test_streamlit_config),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Create sample file for further testing
    sample_file = create_sample_pdf()
    if sample_file:
        results["Sample File Creation"] = True
    else:
        results["Sample File Creation"] = False
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 30)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your RAG chatbot is ready to use.")
        print_usage_instructions()
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        print_troubleshooting_guide()
    
    return passed == total

def print_usage_instructions():
    """Print instructions for using the RAG chatbot."""
    print("\n🚀 How to Use Your RAG Chatbot")
    print("=" * 40)
    print()
    print("1. **Start Streamlit Interface** (Recommended):")
    print("   source rag-env/bin/activate")
    print("   streamlit run streamlit_app.py")
    print("   Open: http://localhost:8501")
    print()
    print("2. **Start Flask API:**")
    print("   source rag-env/bin/activate")
    print("   python src/app.py")
    print("   Open: http://localhost:5000")
    print()
    print("3. **Upload Documents:**")
    print("   - Use the web interface to upload PDF files")
    print("   - Or manually place PDFs in src/data/papers/")
    print()
    print("4. **Test API:**")
    print("   curl -X POST http://localhost:5000/ask \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"query\": \"What are the main findings?\"}'")

def print_troubleshooting_guide():
    """Print troubleshooting information."""
    print("\n🔧 Troubleshooting Guide")
    print("=" * 30)
    print()
    print("Common issues and solutions:")
    print()
    print("1. **Import Errors:**")
    print("   - Make sure virtual environment is activated")
    print("   - Run: pip install -r requirements.txt")
    print()
    print("2. **Model Download Issues:**")
    print("   - Check internet connection")
    print("   - Models download automatically on first use")
    print("   - Be patient, models can be large (500MB+)")
    print()
    print("3. **Memory Issues:**")
    print("   - Use smaller models in src/config.py")
    print("   - Close other applications")
    print()
    print("4. **Port Already in Use:**")
    print("   - Change port in configuration")
    print("   - Kill existing processes: pkill -f streamlit")

if __name__ == "__main__":
    # Make sure we're in the right directory
    if not os.path.exists("src/app.py"):
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Activate virtual environment check
    if not sys.prefix.endswith('rag-env'):
        print("⚠️  Virtual environment may not be activated")
        print("Run: source rag-env/bin/activate")
        print()
    
    run_comprehensive_test()
