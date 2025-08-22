"""
Flask web application for the RAG chatbot API.
"""
from flask import Flask, request, jsonify, render_template_string
import os
from werkzeug.utils import secure_filename
from chatbot import Chatbot

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Initialize the chatbot
papers_dir = os.path.join("data", "papers")
vector_store_dir = os.path.join("data", "vector_store")

chatbot = Chatbot(
    papers_directory=papers_dir,
    vector_store_path=vector_store_dir
)

# Simple HTML template for testing
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Research Paper RAG Chatbot</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .chat-box { border: 1px solid #ddd; height: 400px; overflow-y: auto; padding: 15px; margin: 20px 0; background-color: #fafafa; border-radius: 5px; }
        .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .user-message { background-color: #e3f2fd; text-align: right; }
        .bot-message { background-color: #f1f8e9; }
        .upload-section { margin: 20px 0; padding: 15px; border: 2px dashed #ddd; border-radius: 5px; text-align: center; }
        input[type="text"] { width: 70%; padding: 10px; margin: 10px 5px; border: 1px solid #ddd; border-radius: 5px; }
        input[type="file"] { margin: 10px; }
        button { padding: 10px 20px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        button:hover { background-color: #45a049; }
        .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .status.ready { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .status.not-ready { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .upload-result { padding: 5px; margin: 5px 0; border-radius: 3px; }
        .success { background-color: #d4edda; color: #155724; }
        .error { background-color: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Research Paper RAG Chatbot</h1>
        <div id="status" class="status"></div>
        
        <!-- File Upload Section -->
        <div class="upload-section">
            <h3>📤 Upload Research Papers</h3>
            <input type="file" id="fileInput" multiple accept=".pdf">
            <button onclick="uploadFiles()">Upload Files</button>
            <div id="uploadResults" style="margin-top: 10px;"></div>
        </div>
        
        <div id="chatBox" class="chat-box">
            <div class="message bot-message">
                <strong>Bot:</strong> Hello! I'm ready to answer questions about your research papers. Upload some PDFs or ask questions about existing papers!
            </div>
        </div>
        
        <div>
            <input type="text" id="userInput" placeholder="Ask a question about your papers..." onkeypress="if(event.key==='Enter') sendMessage()">
            <button onclick="sendMessage()">Send</button>
            <button onclick="clearChat()">Clear</button>
        </div>
        
        <div style="margin-top: 20px;">
            <h3>API Endpoints:</h3>
            <ul>
                <li><code>POST /ask</code> - Ask a question</li>
                <li><code>POST /search</code> - Search papers</li>
                <li><code>POST /upload</code> - Upload PDF files</li>
                <li><code>GET /status</code> - Get system status</li>
                <li><code>POST /reload</code> - Reload papers</li>
                <li><code>GET /</code> - This interface</li>
            </ul>
        </div>
    </div>

    <script>
        // Check status on page load
        window.onload = function() {
            checkStatus();
        }
        
        function checkStatus() {
            fetch('/status')
                .then(response => response.json())
                .then(data => {
                    const statusDiv = document.getElementById('status');
                    if (data.ready) {
                        statusDiv.className = 'status ready';
                        statusDiv.innerHTML = `✅ System Ready - ${data.pdf_files_found} PDF files loaded`;
                    } else {
                        statusDiv.className = 'status not-ready';
                        statusDiv.innerHTML = `⚠️ System Not Ready - ${data.pdf_files_found} PDF files found. ${data.vector_store_initialized ? 'Vector store initialized.' : 'Vector store not initialized.'}`;
                    }
                })
                .catch(error => {
                    const statusDiv = document.getElementById('status');
                    statusDiv.className = 'status not-ready';
                    statusDiv.innerHTML = '❌ Error checking status';
                });
        }
        
        function uploadFiles() {
            const fileInput = document.getElementById('fileInput');
            const files = fileInput.files;
            
            if (files.length === 0) {
                alert('Please select files to upload');
                return;
            }
            
            const formData = new FormData();
            for (let i = 0; i < files.length; i++) {
                formData.append('files', files[i]);
            }
            
            const resultsDiv = document.getElementById('uploadResults');
            resultsDiv.innerHTML = '🔄 Uploading files...';
            
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                let resultsHtml = '';
                
                if (data.upload_results) {
                    data.upload_results.forEach(result => {
                        const className = result.status === 'success' ? 'success' : 'error';
                        resultsHtml += `<div class="upload-result ${className}">${result.filename}: ${result.message}</div>`;
                    });
                }
                
                resultsHtml += `<div style="margin-top: 10px;"><strong>${data.message}</strong></div>`;
                resultsDiv.innerHTML = resultsHtml;
                
                // Clear file input
                fileInput.value = '';
                
                // Refresh status
                setTimeout(checkStatus, 1000);
            })
            .catch(error => {
                resultsDiv.innerHTML = '<div class="upload-result error">Error uploading files: ' + error.message + '</div>';
            });
        }
        
        function sendMessage() {
            const input = document.getElementById('userInput');
            const query = input.value.trim();
            
            if (!query) return;
            
            // Add user message to chat
            addMessage('User', query, 'user-message');
            input.value = '';
            
            // Send to API
            fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({query: query})
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    addMessage('Bot', `Error: ${data.error}`, 'bot-message');
                } else {
                    let response = data.response;
                    if (data.source_documents && data.source_documents.length > 0) {
                        response += '<br><br><small><strong>Sources:</strong><br>';
                        data.source_documents.forEach((source, index) => {
                            response += `${index + 1}. ${source}<br>`;
                        });
                        response += '</small>';
                    }
                    addMessage('Bot', response, 'bot-message');
                }
            })
            .catch(error => {
                addMessage('Bot', 'Sorry, there was an error processing your request.', 'bot-message');
            });
        }
        
        function addMessage(sender, message, className) {
            const chatBox = document.getElementById('chatBox');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${className}`;
            messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        
        function clearChat() {
            const chatBox = document.getElementById('chatBox');
            chatBox.innerHTML = '<div class="message bot-message"><strong>Bot:</strong> Chat cleared. How can I help you?</div>';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main interface."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/ask', methods=['POST'])
def ask_question():
    """Handle question asking."""
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({'error': 'No query provided'}), 400
        
        query = data['query']
        result = chatbot.process_query(query)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search', methods=['POST'])
def search_papers():
    """Handle paper searching."""
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({'error': 'No query provided'}), 400
        
        query = data['query']
        k = data.get('k', 5)
        
        results = chatbot.search_papers(query, k=k)
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def get_status():
    """Get chatbot status."""
    try:
        status_info = chatbot.get_status()
        return jsonify(status_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_files():
    """Upload PDF files to the papers directory."""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        if not files:
            return jsonify({'error': 'No files selected'}), 400
        
        results = []
        success_count = 0
        
        # Ensure papers directory exists
        os.makedirs(papers_dir, exist_ok=True)
        
        for file in files:
            if file.filename == '':
                results.append({'filename': '', 'status': 'error', 'message': 'No filename'})
                continue
            
            # Check if file is PDF
            if not file.filename.lower().endswith('.pdf'):
                results.append({
                    'filename': file.filename, 
                    'status': 'error', 
                    'message': 'Only PDF files are allowed'
                })
                continue
            
            try:
                # Secure the filename
                filename = secure_filename(file.filename)
                if not filename:
                    filename = 'uploaded_file.pdf'
                
                # Save file
                file_path = os.path.join(papers_dir, filename)
                file.save(file_path)
                
                results.append({
                    'filename': filename, 
                    'status': 'success', 
                    'message': 'File uploaded successfully'
                })
                success_count += 1
                
            except Exception as e:
                results.append({
                    'filename': file.filename, 
                    'status': 'error', 
                    'message': str(e)
                })
        
        # Reload chatbot if any files were uploaded successfully
        if success_count > 0:
            try:
                global chatbot
                chatbot = Chatbot(
                    papers_directory=papers_dir,
                    vector_store_path=vector_store_dir
                )
            except Exception as e:
                return jsonify({
                    'upload_results': results,
                    'files_uploaded': success_count,
                    'reload_error': str(e)
                }), 500
        
        return jsonify({
            'upload_results': results,
            'files_uploaded': success_count,
            'total_files': len(files),
            'message': f'Successfully uploaded {success_count} out of {len(files)} files'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reload', methods=['POST'])
def reload_papers():
    """Reload papers from directory."""
    try:
        global chatbot
        
        # Reinitialize chatbot
        chatbot = Chatbot(
            papers_directory=papers_dir,
            vector_store_path=vector_store_dir
        )
        
        status_info = chatbot.get_status()
        
        return jsonify({
            'message': 'Papers reloaded successfully',
            'status': status_info
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🤖 Starting Research Paper RAG Chatbot...")
    print(f"📁 Papers directory: {papers_dir}")
    print(f"🗄️ Vector store: {vector_store_dir}")
    print("🌐 App will be available at: http://localhost:5002")
    
    # Create directories if they don't exist
    os.makedirs(papers_dir, exist_ok=True)
    os.makedirs(vector_store_dir, exist_ok=True)
    
    # Check initial status
    status_info = chatbot.get_status()
    print(f"📊 Status: {'Ready' if status_info['ready'] else 'Not Ready'}")
    print(f"📄 PDF files found: {status_info['pdf_files_found']}")
    
    if not status_info['ready']:
        print(f"\n⚠️  To get started:")
        print(f"   1. Add PDF research papers to: {papers_dir}")
        print(f"   2. Restart the application or use /reload endpoint")
        print(f"   3. Or use the web interface to upload files")
    
    app.run(host='0.0.0.0', port=5002, debug=True)