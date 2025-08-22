"""
Streamlit web application for the RAG chatbot.
"""
import streamlit as st
import os
import sys
from datetime import datetime

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import Chatbot
from utils.helpers import format_response, get_file_info


def initialize_chatbot():
    """Initialize the chatbot with session state."""
    if 'chatbot' not in st.session_state:
        papers_dir = os.path.join("src", "data", "papers")
        vector_store_dir = os.path.join("src", "data", "vector_store")
        
        st.session_state.chatbot = Chatbot(
            papers_directory=papers_dir,
            vector_store_path=vector_store_dir
        )
    
    return st.session_state.chatbot


def display_status(chatbot):
    """Display chatbot status in sidebar."""
    status = chatbot.get_status()
    
    st.sidebar.header("📊 System Status")
    
    if status['ready']:
        st.sidebar.success("✅ Ready to answer questions!")
    else:
        st.sidebar.warning("⚠️ System not ready")
    
    st.sidebar.write(f"**PDF Files Found:** {status['pdf_files_found']}")
    st.sidebar.write(f"**Vector Store:** {'✅ Initialized' if status['vector_store_initialized'] else '❌ Not initialized'}")
    
    # Papers directory info
    if os.path.exists(status['papers_directory']):
        st.sidebar.write(f"**Papers Directory:** {status['papers_directory']}")
    else:
        st.sidebar.error(f"Papers directory not found: {status['papers_directory']}")


def main():
    st.set_page_config(
        page_title="Research Paper RAG Chatbot",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Research Paper RAG Chatbot")
    st.markdown("Ask questions about your research papers using AI-powered retrieval and generation!")
    
    # Initialize chatbot
    chatbot = initialize_chatbot()
    
    # Display status
    display_status(chatbot)
    
    # Main interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.header("💬 Chat Interface")
        
        # Chat history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for i, chat in enumerate(st.session_state.chat_history):
                # User message
                st.markdown(f"**You:** {chat['query']}")
                
                # Bot response
                st.markdown(f"**Bot:** {chat['response']}")
                
                # Sources (if any)
                if chat.get('sources'):
                    with st.expander("📚 View Sources"):
                        for j, source in enumerate(chat['sources'], 1):
                            st.write(f"{j}. {source}")
                
                st.divider()
        
        # Query input
        with st.form("chat_form", clear_on_submit=True):
            user_query = st.text_area(
                "Ask a question about your research papers:",
                height=100,
                placeholder="e.g., What are the main findings about machine learning in the papers?"
            )
            
            col_submit, col_clear = st.columns([1, 1])
            
            with col_submit:
                submit_button = st.form_submit_button("🚀 Ask Question", use_container_width=True)
            
            with col_clear:
                if st.form_submit_button("🗑️ Clear History", use_container_width=True):
                    st.session_state.chat_history = []
                    st.rerun()
        
        # Process query
        if submit_button and user_query:
            with st.spinner("🔍 Searching papers and generating response..."):
                try:
                    result = chatbot.process_query(user_query)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        'query': user_query,
                        'response': result['response'],
                        'sources': result.get('source_documents', []),
                        'timestamp': datetime.now().strftime("%H:%M:%S")
                    })
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error processing query: {str(e)}")
    
    with col2:
        st.header("🔍 Quick Search")
        
        # Search functionality
        search_query = st.text_input(
            "Search papers:",
            placeholder="Enter keywords..."
        )
        
        search_k = st.slider("Number of results:", 1, 10, 5)
        
        if st.button("🔍 Search", use_container_width=True) and search_query:
            with st.spinner("Searching..."):
                try:
                    search_results = chatbot.search_papers(search_query, k=search_k)
                    
                    if search_results['results']:
                        st.success(f"Found {len(search_results['results'])} results")
                        
                        for i, result in enumerate(search_results['results'], 1):
                            with st.expander(f"Result {i} - {result['source']}"):
                                st.write(f"**Source:** {result['source']}")
                                st.write(f"**Page:** {result.get('page', 'Unknown')}")
                                st.write(f"**Similarity:** {result['similarity_score']:.3f}")
                                st.write("**Content:**")
                                st.write(result['content'][:300] + "..." if len(result['content']) > 300 else result['content'])
                    else:
                        st.info("No results found")
                        
                except Exception as e:
                    st.error(f"Search error: {str(e)}")
        
        st.divider()
        
        # File management
        st.header("📁 File Management")
        
        # File Upload Section
        st.subheader("📤 Upload Documents")
        uploaded_files = st.file_uploader(
            "Upload PDF research papers",
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload one or more PDF files to add to your knowledge base"
        )
        
        if uploaded_files:
            if st.button("💾 Save Uploaded Files", use_container_width=True):
                success_count = 0
                error_count = 0
                papers_dir = os.path.join("src", "data", "papers")
                
                # Ensure directory exists
                os.makedirs(papers_dir, exist_ok=True)
                
                with st.spinner("Saving uploaded files..."):
                    for uploaded_file in uploaded_files:
                        try:
                            # Save file to papers directory
                            file_path = os.path.join(papers_dir, uploaded_file.name)
                            with open(file_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            success_count += 1
                            st.success(f"✅ Saved: {uploaded_file.name}")
                        except Exception as e:
                            error_count += 1
                            st.error(f"❌ Failed to save {uploaded_file.name}: {str(e)}")
                    
                    # Reload chatbot with new files
                    if success_count > 0:
                        try:
                            st.session_state.chatbot.load_papers()
                            st.success(f"🔄 Reloaded chatbot with {success_count} new files!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error reloading chatbot: {str(e)}")
        
        st.divider()
        
        # Show papers directory
        st.subheader("📂 Current Documents")
        papers_dir = os.path.join("src", "data", "papers")
        
        if not os.path.exists(papers_dir):
            st.warning("Papers directory doesn't exist. Creating it...")
            os.makedirs(papers_dir, exist_ok=True)
        
        # List existing PDF files
        pdf_files = [f for f in os.listdir(papers_dir) if f.lower().endswith('.pdf')]
        
        if pdf_files:
            st.success(f"Found {len(pdf_files)} PDF files:")
            for pdf in pdf_files:
                file_info = get_file_info(os.path.join(papers_dir, pdf))
                col_file, col_delete = st.columns([3, 1])
                with col_file:
                    st.write(f"📄 {pdf} ({file_info['size_mb']} MB)")
                with col_delete:
                    if st.button("🗑️", key=f"delete_{pdf}", help=f"Delete {pdf}"):
                        try:
                            os.remove(os.path.join(papers_dir, pdf))
                            st.success(f"Deleted {pdf}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting file: {str(e)}")
        else:
            st.info("No PDF files found. Upload some documents to get started!")
        
        # Refresh button
        if st.button("🔄 Reload Papers", use_container_width=True):
            with st.spinner("Reloading papers..."):
                try:
                    # Reinitialize chatbot
                    st.session_state.chatbot = Chatbot(
                        papers_directory=papers_dir,
                        vector_store_path=os.path.join("src", "data", "vector_store")
                    )
                    st.success("Papers reloaded successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error reloading papers: {str(e)}")


if __name__ == "__main__":
    main()
