#!/bin/bash

# Quick start script for RAG Demo

echo "🚀 RAG Demo Quick Start"
echo "======================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ pip is required but not installed."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env file with your API keys:"
    echo "   - PINECONE_API_KEY"
    echo "   - GROQ_API_KEY" 
    echo "   - COHERE_API_KEY"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Run tests
echo "🧪 Running system tests..."
python test_setup.py

echo ""
echo "🎉 Setup complete! Run the application with:"
echo "   streamlit run app.py"
