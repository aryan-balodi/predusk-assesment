# RAG Demo - Document Q&A System (Track B)

A Retrieval-Augmented Generation (RAG) application that allows users to upload documents and ask questions, receiving answers with source citations.

**📄 Resume**: [View Resume](https://drive.google.com/file/d/1LteXSfKIKkFtBsW5Ez_EgrAyC9Tyg-3W/view?usp=sharing)

**🔗 Live Demo**: [View Live Demo](https://ragpipelinesearch.streamlit.app/)

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
- **Vector Search**: Pinecone cloud-hosted vector database with local embeddings
- **Reranking**: Cohere Rerank API for improved relevance
- **LLM Integration**: Groq Cloud for fast answer generation
- **Source Citations**: Inline citations with source mapping
- **Performance Metrics**: Query timing and token usage tracking

## 📋 Requirements Met

### ✅ Vector Database (Hosted)
- **Service**: Pinecone cloud vector database
- **Model**: sentence-transformers/all-mpnet-base-v2 (local embedding)
- **Dimension**: 768
- **Strategy**: Local embedding with SentenceTransformers, stored in Pinecone

### ✅ Embeddings & Chunking  
- **Chunking**: 1000-1200 tokens with 15% overlap
- **Metadata**: Source, title, section, position stored for precise citations
- **Section Detection**: Automatic section identification from headers and structure
- **Title Extraction**: Smart title detection from document content
- **Embedding**: SentenceTransformers all-mpnet-base-v2 (768D local embeddings)

### ✅ Retriever + Reranker
- **Retrieval**: Top-20 MMR from Pinecone vector DB
- **Reranker**: Cohere Rerank API (rerank-english-v3.0)
- **Fallback**: Score-based reranker if Cohere unavailable

### ✅ LLM & Answering
- **Provider**: Groq Cloud (fast inference)
- **Model**: llama-3.1-8b-instant
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
PINECONE_INDEX_NAME=predusk-demo-v2
```

### 3. Pinecone Index Setup

Create a Pinecone index with these settings:
- **Name**: `predusk-demo-v2`
- **Dimension**: `768`
- **Metric**: `cosine`
- **Cloud**: `AWS`
- **Region**: `us-east-1`
- **Note**: No auto-embedding needed (using local SentenceTransformers)

#### Index Details & Current Status
- **Index Name**: `predusk-demo-v2`
- **Vector Count**: ~1700 vectors (from Cisco SDMH24.pdf documentation)
- **Storage Used**: ~5.08 MB estimated
- **Embedding Model**: sentence-transformers/all-mpnet-base-v2
- **Vector Dimension**: 768
- **Metadata Fields**: source, title, section, position, text
- **Created**: Ready for demo with pre-loaded Cisco documentation
- **Backup Content**: Sample AI/ML content available for direct text input testing

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
- **Model**: llama-3.1-8b-instant (Groq)
- **Max Tokens**: 1000
- **Temperature**: 0.1 (focused responses)

## 📚 Example Q&A Pairs

**Note**: Current vector database contains Cisco Router documentation. Use these questions for testing:

### 1. **Cisco SDM Overview**
**Q**: "What is the Cisco Router and Security Device Manager?"
**Expected**: Explanation of SDM as a web-based configuration tool for Cisco routers

### 2. **VPN Configuration**  
**Q**: "How do you configure VPN settings using SDM?"
**Expected**: Description of VPN configuration steps and available options

### 3. **Security Features**
**Q**: "What security features are available in Cisco SDM?"
**Expected**: Information about firewall, VPN, intrusion prevention, and security auditing

### 4. **System Requirements**
**Q**: "What are the system requirements for running SDM?"
**Expected**: Browser requirements, Java versions, and supported operating systems

### 5. **Alternative Content Testing**
**Q**: Use the sample AI/ML content in `sample_document.md` via Direct Text Input
**Expected**: Test with questions like "What are the types of AI?" after adding content

## 🔧 Architecture Details

### Document Processing Pipeline
1. **Upload**: PDF/TXT file processing
2. **Extraction**: Text extraction with metadata
3. **Chunking**: Overlapping chunks with context preservation
4. **Embedding**: Local embedding via SentenceTransformers (all-mpnet-base-v2)
5. **Storage**: Vector storage with metadata in Pinecone

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
1. **Local vs Cloud Embedding**: Chose local SentenceTransformers for consistency and control
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
   PINECONE_INDEX_NAME = "predusk-demo-v2"
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
PINECONE_INDEX_NAME=<default: predusk-demo-v2>
```

### Health Checks
The application includes built-in connectivity checks for:
- Pinecone vector database connection
- Groq LLM API availability  
- Cohere reranker service (with fallback)

---

## 📝 Remarks

### Provider Limitations & Considerations

#### **Pinecone (Vector Database)**
- **Free Tier**: 1 index, 100K vectors, 10MB storage
- **Performance**: ~200-500ms query latency
- **Scalability**: Excellent for production use
- **Cost**: Usage-based pricing after free tier

#### **Groq (LLM Provider)**
- **Speed**: Fastest inference (~1-3s for responses)
- **Rate Limits**: 30 requests/minute on free tier
- **Model**: llama-3.1-8b-instant optimized for speed
- **Quality**: Good balance of speed vs. accuracy

#### **Cohere (Reranker)**
- **Free Tier**: 1000 API calls/month
- **Fallback**: Local score-based reranker when unavailable
- **Language**: Optimized for English content
- **Performance**: ~300-800ms reranking latency

#### **SentenceTransformers (Embeddings)**
- **Model**: all-mpnet-base-v2 (768 dimensions)
- **Advantages**: Consistent, local processing, no API costs
- **Performance**: Fast local embedding generation
- **Quality**: High-quality semantic representations

### Architecture Decisions

1. **Local Embeddings**: Chose SentenceTransformers over cloud embedding APIs for consistency, cost control, and reduced external dependencies.

2. **Groq LLM**: Selected for fastest inference time, crucial for interactive demo experience.

3. **Hybrid Reranking**: Implemented fallback reranker to ensure system works even without Cohere API access.

4. **Streamlit Frontend**: Rapid prototyping and deployment, perfect for demo applications with built-in hosting support.

---

**Built for**: AI Engineer Assessment - Mini RAG System (Track B)  
**Tech Stack**: Streamlit + Pinecone + Cohere + Groq + SentenceTransformers  
**Deployment Ready**: ✅ All requirements met  
**Resume**: [View Resume](https://example.com/your-resume.pdf)
