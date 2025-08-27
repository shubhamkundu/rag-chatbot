#!/usr/bin/env python3
"""
Setup script for the RAG Chatbot.
"""
import os
import sys
import subprocess


def create_directories():
    """Create necessary directories."""
    directories = [
        "src/data/papers",
        "src/data/vector_store"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")


def create_sample_readme():
    """Create a README in the papers directory."""
    papers_readme = """# Research Papers Directory

## Getting Started

1. **Add PDF Files**: Place your research papers (PDF format) in this directory
2. **Supported Formats**: Only PDF files are currently supported
3. **File Names**: Use descriptive names for better organization

## Example Papers

You can download sample research papers from:
- arXiv.org
- Google Scholar
- PubMed
- IEEE Xplore
- ResearchGate

## Tips

- Keep file names descriptive and without special characters
- Papers should be text-based PDFs (not scanned images for best results)
- The system will automatically process new papers when you restart the application

## Current Papers

(Add your papers here and they will be automatically detected)
"""
    
    readme_path = "src/data/papers/README.md"
    with open(readme_path, "w") as f:
        f.write(papers_readme)
    
    print(f"✅ Created: {readme_path}")


def install_dependencies():
    """Install Python dependencies."""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    return True


def main():
    """Main setup function."""
    print("🚀 Setting up RAG Chatbot...")
    
    # Create directories
    create_directories()
    
    # Create sample README
    create_sample_readme()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed due to dependency installation error.")
        return
    
    print("\n✅ Setup completed successfully!")
    print("\n🎯 Next Steps:")
    print("1. Add PDF research papers to: src/data/papers/")
    print("2. Run the Flask app: python src/app.py")
    print("3. Or run the Streamlit app: streamlit run streamlit_app.py")
    print("\n📚 Documentation:")
    print("- Flask API will be available at: http://localhost:5001")
    print("- Streamlit interface will be available at: http://localhost:8501")
    
    # Check for existing papers
    papers_dir = "src/data/papers"
    pdf_files = [f for f in os.listdir(papers_dir) if f.lower().endswith('.pdf')]
    
    if pdf_files:
        print(f"\n📄 Found {len(pdf_files)} existing PDF files:")
        for pdf in pdf_files:
            print(f"   - {pdf}")
    else:
        print(f"\n📝 No PDF files found. Add your research papers to {papers_dir} to get started!")


if __name__ == "__main__":
    main()
