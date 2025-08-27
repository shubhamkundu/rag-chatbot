#!/usr/bin/env python3
"""
Simple test script that works without downloading large models.
"""
import os
import sys

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_without_models():
    """Test the system without loading heavy ML models."""
    print("🤖 RAG Chatbot - Lightweight Test")
    print("=" * 40)
    
    # Test document loader
    print("\n📄 Testing document processing...")
    try:
        from document_loader import DocumentLoader
        loader = DocumentLoader()
        
        # Check if we have sample documents
        papers_dir = "src/data/papers"
        text_files = [f for f in os.listdir(papers_dir) if f.endswith('.txt')]
        pdf_files = [f for f in os.listdir(papers_dir) if f.endswith('.pdf')]
        
        print(f"✅ Found {len(text_files)} text files and {len(pdf_files)} PDF files")
        
        # Test text processing
        sample_text = """
        This is a sample research paper about machine learning.
        The methodology involves using neural networks for classification.
        Results show 95% accuracy on the test dataset.
        Conclusion: The approach is effective for this domain.
        """
        
        processed_text = loader.preprocess_text(sample_text)
        print(f"✅ Text preprocessing works: {len(processed_text)} characters")
        
        return True
    except Exception as e:
        print(f"❌ Document processing error: {e}")
        return False

def create_simple_flask_demo():
    """Create a simple Flask demo that works without ML models."""
    print("\n🌐 Creating simple Flask demo...")
    
    demo_content = '''
from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

# Simple HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>RAG Chatbot - Demo Mode</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
        .status { padding: 10px; margin: 10px 0; border-radius: 5px; background-color: #d4edda; color: #155724; }
        input[type="text"] { width: 70%; padding: 10px; margin: 10px 5px; border: 1px solid #ddd; border-radius: 5px; }
        button { padding: 10px 20px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 RAG Chatbot - Demo Mode</h1>
        <div class="status">
            ✅ System is running in demo mode (models not loaded)
        </div>
        
        <h3>📊 System Information</h3>
        <p><strong>Papers Directory:</strong> {{ papers_dir }}</p>
        <p><strong>Files Found:</strong> {{ file_count }} files</p>
        <p><strong>Mode:</strong> Demo (without ML models)</p>
        
        <h3>💬 Test Query</h3>
        <form action="/demo_ask" method="post">
            <input type="text" name="query" placeholder="Ask a test question..." value="What are the main findings?">
            <button type="submit">Ask</button>
        </form>
        
        {% if response %}
        <div style="margin-top: 20px; padding: 15px; background-color: #f8f9fa; border-radius: 5px;">
            <strong>Response:</strong> {{ response }}
        </div>
        {% endif %}
        
        <h3>📝 Next Steps</h3>
        <ul>
            <li>Add PDF research papers to the papers directory</li>
            <li>Install and configure ML models for full functionality</li>
            <li>Test with real document queries</li>
        </ul>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    papers_dir = "src/data/papers"
    file_count = len([f for f in os.listdir(papers_dir) if f.endswith(('.pdf', '.txt'))])
    return render_template_string(HTML_TEMPLATE, 
                                papers_dir=papers_dir, 
                                file_count=file_count,
                                response=None)

@app.route('/demo_ask', methods=['POST'])
def demo_ask():
    query = request.form.get('query', '')
    
    # Simple demo response
    demo_responses = {
        "main findings": "Demo: The main findings include improved accuracy and efficiency in document processing.",
        "methodology": "Demo: The methodology uses retrieval-augmented generation with vector databases.",
        "results": "Demo: Results show successful implementation of the RAG pipeline architecture.",
        "default": f"Demo: You asked about '{query}'. In a full system, this would search through your uploaded documents and provide detailed answers based on the content."
    }
    
    # Find matching response
    response = demo_responses["default"]
    for key, value in demo_responses.items():
        if key in query.lower():
            response = value
            break
    
    papers_dir = "src/data/papers"
    file_count = len([f for f in os.listdir(papers_dir) if f.endswith(('.pdf', '.txt'))])
    
    return render_template_string(HTML_TEMPLATE, 
                                papers_dir=papers_dir, 
                                file_count=file_count,
                                response=response)

@app.route('/status')
def status():
    papers_dir = "src/data/papers"
    file_count = len([f for f in os.listdir(papers_dir) if f.endswith(('.pdf', '.txt'))])
    
    return jsonify({
        "status": "demo_mode",
        "papers_directory": papers_dir,
        "pdf_files_found": file_count,
        "vector_store_initialized": False,
        "ready": True,
        "mode": "Demo (models not loaded)"
    })

if __name__ == '__main__':
    print("🚀 Starting RAG Chatbot Demo...")
    print("📁 Papers directory: src/data/papers")
    print("🌐 Demo will be available at: http://localhost:5001")
    print("💡 This is a demo mode without ML models loaded")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
'''
    
    with open("demo_flask.py", "w") as f:
        f.write(demo_content)
    
    print("✅ Simple Flask demo created: demo_flask.py")
    return True

def show_options():
    """Show user options for testing the system."""
    print("\n🚀 Your RAG Chatbot Test Options")
    print("=" * 40)
    print()
    print("Option 1: Run Demo Mode (No model downloads)")
    print("  Command: source rag-env/bin/activate && python demo_flask.py")
    print("  URL: http://localhost:5001")
    print("  Features: Basic interface, file detection, demo responses")
    print()
    print("Option 2: Full System (Requires model downloads ~500MB)")
    print("  Command: source rag-env/bin/activate && python src/app.py")
    print("  URL: http://localhost:5001")
    print("  Features: Full RAG functionality, real AI responses")
    print()
    print("Option 3: Streamlit Interface")
    print("  Command: source rag-env/bin/activate && streamlit run streamlit_app.py")
    print("  URL: http://localhost:8501")
    print("  Features: Modern UI, file upload, chat interface")
    print()
    print("📋 Current Status:")
    papers_dir = "src/data/papers"
    if os.path.exists(papers_dir):
        files = [f for f in os.listdir(papers_dir) if f.endswith(('.pdf', '.txt'))]
        print(f"  📄 Files in papers directory: {len(files)}")
        if files:
            for f in files[:3]:  # Show first 3 files
                print(f"    - {f}")
            if len(files) > 3:
                print(f"    ... and {len(files) - 3} more")
    else:
        print("  📄 Papers directory not found")

if __name__ == "__main__":
    success = test_without_models()
    
    if success:
        create_simple_flask_demo()
        show_options()
    else:
        print("❌ Basic tests failed. Please check the setup.")
