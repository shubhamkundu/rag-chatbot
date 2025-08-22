
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
