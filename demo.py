#!/usr/bin/env python3
"""
Demo script for the RAG Chatbot.
Run this to test the chatbot functionality with sample queries.
"""
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import Chatbot
from utils.helpers import format_response


def demo_queries():
    """Sample queries to demonstrate the chatbot."""
    return [
        "What are the main findings in the research papers?",
        "What methodologies were used in the studies?",
        "What datasets were mentioned in the papers?",
        "What are the key conclusions?",
        "What future work is suggested?",
    ]


def run_demo():
    """Run the chatbot demo."""
    print("🤖 RAG Chatbot Demo")
    print("=" * 50)
    
    # Initialize chatbot
    print("📚 Initializing chatbot...")
    papers_dir = os.path.join("src", "data", "papers")
    vector_store_dir = os.path.join("src", "data", "vector_store")
    
    chatbot = Chatbot(
        papers_directory=papers_dir,
        vector_store_path=vector_store_dir
    )
    
    # Check status
    status = chatbot.get_status()
    print(f"📊 Status: {'Ready' if status['ready'] else 'Not Ready'}")
    print(f"📄 PDF files found: {status['pdf_files_found']}")
    
    if not status['ready']:
        print("\n❌ Demo cannot run - no papers found!")
        print(f"📁 Please add PDF papers to: {papers_dir}")
        print("💡 After adding papers, run this demo again.")
        return
    
    print(f"✅ Found {status['pdf_files_found']} papers. Ready to chat!")
    print("\n" + "=" * 50)
    
    # Interactive mode or demo mode
    mode = input("\nChoose mode:\n1. Interactive (you ask questions)\n2. Demo (predefined questions)\nEnter 1 or 2: ").strip()
    
    if mode == "1":
        interactive_mode(chatbot)
    else:
        demo_mode(chatbot)


def interactive_mode(chatbot):
    """Run in interactive mode."""
    print("\n🔄 Interactive Mode - Type 'quit' to exit")
    print("-" * 40)
    
    while True:
        query = input("\n💭 Your question: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("👋 Thanks for using the RAG Chatbot!")
            break
        
        if not query:
            continue
        
        print("\n🔍 Searching and generating response...")
        
        try:
            result = chatbot.process_query(query)
            
            print(f"\n🤖 Answer:")
            print("-" * 40)
            print(result['response'])
            
            if result.get('source_documents'):
                print(f"\n📚 Sources:")
                for i, source in enumerate(result['source_documents'], 1):
                    print(f"{i}. {source[:100]}...")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")


def demo_mode(chatbot):
    """Run predefined demo queries."""
    print("\n🎭 Demo Mode - Running sample queries")
    print("-" * 40)
    
    queries = demo_queries()
    
    for i, query in enumerate(queries, 1):
        print(f"\n📝 Query {i}: {query}")
        print("-" * 40)
        
        try:
            result = chatbot.process_query(query)
            
            print(f"🤖 Answer: {result['response'][:300]}...")
            
            if result.get('source_documents'):
                print(f"📚 Found {len(result['source_documents'])} relevant sources")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        if i < len(queries):
            input("\nPress Enter to continue to next query...")
    
    print(f"\n✅ Demo completed! Tested {len(queries)} queries.")


def search_demo(chatbot):
    """Demonstrate search functionality."""
    print("\n🔍 Search Demo")
    print("-" * 30)
    
    search_terms = [
        "machine learning",
        "neural networks", 
        "accuracy",
        "dataset",
        "methodology"
    ]
    
    for term in search_terms:
        print(f"\n🔎 Searching for: '{term}'")
        
        try:
            results = chatbot.search_papers(term, k=3)
            print(f"📊 Found {len(results['results'])} results")
            
            for i, result in enumerate(results['results'], 1):
                print(f"  {i}. {result['source']} (Score: {result['similarity_score']:.3f})")
                
        except Exception as e:
            print(f"❌ Search error: {str(e)}")


if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Demo error: {str(e)}")
        print("💡 Make sure you've run setup.py and added PDF papers to src/data/papers/")
