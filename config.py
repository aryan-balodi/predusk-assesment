"""
Configuration and utility functions for the RAG application
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_config_value(key, default=None):
    """Get configuration value from environment or Streamlit secrets"""
    try:
        import streamlit as st
        # Try Streamlit secrets first (for cloud deployment)
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key]
    except ImportError:
        pass
    # Fallback to environment variables
    return os.getenv(key, default)

# API Keys
PINECONE_API_KEY = get_config_value("PINECONE_API_KEY")
GROQ_API_KEY = get_config_value("GROQ_API_KEY") 
COHERE_API_KEY = get_config_value("COHERE_API_KEY")

# Pinecone Configuration
PINECONE_INDEX_NAME = get_config_value("PINECONE_INDEX_NAME", "predusk-demo")
PINECONE_ENVIRONMENT = get_config_value("PINECONE_ENVIRONMENT", "us-east-1")

# Chunking Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150  # 15% overlap

# Retrieval Configuration
TOP_K_RETRIEVAL = 20
TOP_K_RERANK = 5

# LLM Configuration
LLM_MODEL = "llama-3.1-8b-instant"  # Groq model
MAX_TOKENS = 1000
TEMPERATURE = 0.1
