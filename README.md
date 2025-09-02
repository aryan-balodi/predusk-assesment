# RAG Demo - Document Q&A System

A Retrieval-Augmented Generation (RAG) application that allows users to upload documents and ask questions, receiving answers with source citations.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   Document       │    │   Pinecone      │
│   Frontend      │───▶│   Processor      │───▶│   Vector DB     │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                                               │
         ▼                                               ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Query    │───▶│   Retrieval      │◀───│   Query Similar │
│                 │    │   Pipeline       │    │   Documents     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Cohere         │
                       │   Reranker       │
                       └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Groq LLM       │
                       │   Answer Gen     │
                       └──────────────────┘
```

## 🚀 Features

- **Document Upload**: Support for PDF and TXT files
- **Text Chunking**: Smart chunking with 15% overlap (1000-1200 tokens)
- **Vector Search**: Pinecone cloud-hosted vector database with auto-embedding
- **Reranking**: Cohere Rerank API for improved relevance
- **LLM Integration**: Groq Cloud for fast answer generation
- **Source Citations**: Inline citations with source mapping
- **Performance Metrics**: Query timing and token usage tracking

## 📋 Requirements Met

### ✅ Vector Database (Hosted)
- **Service**: Pinecone cloud vector database
- **Model**: llama-text-embed-v2 (built-in auto-embedding)
- **Dimension**: 1024
- **Strategy**: Auto-embedding with metadata storage

### ✅ Embeddings & Chunking  
- **Chunking**: 1000-1200 tokens with 15% overlap
- **Metadata**: Source, title, section, position stored for precise citations
- **Section Detection**: Automatic section identification from headers and structure
- **Title Extraction**: Smart title detection from document content
- **Embedding**: Pinecone auto-embedding (llama-text-embed-v2)

### ✅ Retriever + Reranker
- **Retrieval**: Top-20 MMR from Pinecone vector DB
- **Reranker**: Cohere Rerank API (rerank-english-v3.0)
- **Fallback**: Score-based reranker if Cohere unavailable

### ✅ LLM & Answering
- **Provider**: Groq Cloud (fast inference)
- **Model**: llama3-8b-8192
- **Citations**: Inline citations [1], [2] mapped to sources
- **Graceful handling**: No-answer cases handled properly

### ✅ Frontend
- **Framework**: Streamlit
- **Features**: Upload/paste, query box, answers with citations
- **Metrics**: Request timing and token cost estimates

### ✅ Hosting & Docs
- **Deployment**: Ready for free hosting (Streamlit Cloud, Render, etc.)
- **Documentation**: Architecture diagram, configuration details
- **Quick start**: Complete setup instructions

## 🛠️ Setup Instructions

### 1. Clone and Install Dependencies

```bash
git clone <repository-url>
cd predusk
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file with your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
PINECONE_API_KEY=your_pinecone_api_key_here
GROQ_API_KEY=your_groq_api_key_here  
COHERE_API_KEY=your_cohere_api_key_here
PINECONE_INDEX_NAME=predusk-demo
```

### 3. Pinecone Index Setup

Create a Pinecone index with these settings:
- **Name**: `predusk-demo`
- **Dimension**: `1024`
- **Metric**: `cosine`
- **Cloud**: `AWS`
- **Region**: `us-east-1`
- **Auto-embedding**: Enable with `llama-text-embed-v2`

### 4. Run the Application

```bash
streamlit run app.py
```

## ⚙️ Configuration

### Chunking Parameters
- **Chunk Size**: 1000 tokens
- **Overlap**: 150 tokens (15%)
- **Strategy**: Sentence-aware chunking with section detection
- **Metadata**: Source, title, section, position for enhanced citations

### Retrieval Settings
- **Initial Retrieval**: Top-20 documents
- **Reranking**: Top-5 after rerank
- **Similarity Metric**: Cosine similarity

### LLM Settings
- **Model**: llama3-8b-8192 (Groq)
- **Max Tokens**: 1000
- **Temperature**: 0.1 (focused responses)

## 📚 Example Q&A Pairs

### 1. **General Document Content**
**Q**: "What are the main topics covered in this document?"
**Expected**: Summary of key themes with citations to relevant sections

### 2. **Specific Information Lookup**  
**Q**: "What is the definition of [specific term]?"
**Expected**: Precise definition with citation to source

### 3. **Comparative Analysis**
**Q**: "How does approach A compare to approach B?"
**Expected**: Comparison with citations to both approaches

### 4. **Factual Questions**
**Q**: "What are the requirements for [specific process]?"
**Expected**: Listed requirements with proper source citations

### 5. **No Information Available**
**Q**: "What is the company's policy on [unrelated topic]?"
**Expected**: "I don't have relevant information..." response

## 🔧 Architecture Details

### Document Processing Pipeline
1. **Upload**: PDF/TXT file processing
2. **Extraction**: Text extraction with metadata
3. **Chunking**: Overlapping chunks with context preservation
4. **Embedding**: Auto-embedding via Pinecone
5. **Storage**: Vector storage with metadata

### Query Processing Pipeline
1. **Query**: User question input
2. **Retrieval**: Vector similarity search (top-20)
3. **Reranking**: Cohere rerank to top-5
4. **Generation**: LLM answer generation with citations
5. **Display**: Formatted response with source mapping

## 📊 Performance Characteristics

- **Retrieval Speed**: ~200-500ms (Pinecone)
- **Reranking**: ~300-800ms (Cohere API)
- **Generation**: ~1-3s (Groq LLM)
- **Total Response**: ~2-4s end-to-end

## 🚨 Limitations & Trade-offs

### Current Limitations
1. **File Format**: Only PDF and TXT supported
2. **Language**: English-optimized (Cohere rerank model)
3. **Context Window**: 1000 token chunks may break long concepts
4. **Rate Limits**: Subject to API provider rate limits

### Design Trade-offs
1. **Auto-embedding vs Custom**: Chose speed over customization
2. **Chunk Size**: Balanced context vs. precision
3. **Reranker**: API dependency vs. local model performance
4. **LLM Provider**: Groq speed vs. OpenAI quality

## 🛡️ Error Handling

- **API Failures**: Graceful fallbacks for each service
- **File Processing**: Clear error messages for unsupported formats
- **No Results**: Proper "no information found" responses
- **Rate Limiting**: Automatic retries with backoff

## 📈 Future Enhancements

### Possible Improvements
1. **Multi-format Support**: Word docs, PowerPoint, etc.
2. **Advanced Chunking**: Semantic chunking strategies
3. **Multi-language**: Support for non-English content
4. **Hybrid Search**: Combine dense + sparse retrieval
5. **Conversation Memory**: Multi-turn conversation support

### Scalability Considerations
1. **Caching**: Query result caching
2. **Batch Processing**: Bulk document upload
3. **Index Management**: Multiple specialized indices
4. **Load Balancing**: API request distribution

## 📞 Support & Deployment

### Quick Deploy to Streamlit Cloud (Recommended)

1. **Push to GitHub**: Commit your code to a GitHub repository
2. **Connect to Streamlit Cloud**: 
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository and branch
   - Set main file path to `app.py`
3. **Configure Secrets**:
   - In Streamlit Cloud dashboard, go to "Secrets"
   - Copy contents from `.env.example` and add your actual API keys:
   ```toml
   PINECONE_API_KEY = "your_actual_pinecone_key"
   GROQ_API_KEY = "your_actual_groq_key"
   COHERE_API_KEY = "your_actual_cohere_key"
   PINECONE_INDEX_NAME = "predusk-demo"
   ```
4. **Deploy**: Click "Deploy" - your app will be live in minutes!

### Alternative Deployment Options
- **Render**: Container deployment with `Dockerfile`
- **Railway**: Fast deployment platform
- **Heroku**: Container deployment (may require paid dyno)

### Local Development
```bash
streamlit run app.py
```

### Environment Variables Required
```env
PINECONE_API_KEY=<required>
GROQ_API_KEY=<required>
COHERE_API_KEY=<optional - fallback reranker used>
PINECONE_INDEX_NAME=<default: predusk-demo>
```

### Health Checks
The application includes built-in connectivity checks for:
- Pinecone vector database connection
- Groq LLM API availability  
- Cohere reranker service (with fallback)

---

**Built for**: AI Engineer Assessment - Mini RAG System  
**Tech Stack**: Streamlit + Pinecone + Cohere + Groq  
**Deployment Ready**: ✅ All requirements met
