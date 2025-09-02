"""
Modern Streamlit application for the RAG system with enhanced UI
"""
import streamlit as st
import time
from typing import List, Dict, Any
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config FIRST, before any other Streamlit commands
st.set_page_config(
    page_title="🔍 RAG Demo - Document Q&A",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern dark theme
st.markdown("""
<style>
    /* Force full width layout - most important rules */
    .main .block-container {
        max-width: none !important;
        width: 100% !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 1rem !important;
    }
    
    /* Main container styling */
    .main > div {
        padding-top: 1rem;
        width: 100% !important;
        max-width: none !important;
    }
    
    /* Critical: Control sidebar width and main content area */
    .css-1d391kg {
        flex: 0 0 300px !important;
        width: 300px !important;
        max-width: 300px !important;
    }
    
    /* Main content area should take remaining space */
    .main {
        flex: 1 !important;
        width: calc(100% - 300px) !important;
        max-width: none !important;
    }
    
    /* Force all element containers to use full width */
    .element-container {
        width: 100% !important;
        max-width: none !important;
    }
    
    /* App container and main layout control */
    .stApp {
        max-width: none !important;
    }
    
    .stApp > div:first-child {
        display: flex !important;
        width: 100% !important;
        max-width: none !important;
    }
    
    /* Ensure sidebar stays fixed width */
    section[data-testid="stSidebar"] {
        width: 300px !important;
        min-width: 300px !important;
        max-width: 300px !important;
        flex: 0 0 300px !important;
    }
    
    /* Main content should use all remaining space */
    section.main {
        flex: 1 !important;
        width: calc(100vw - 300px) !important;
        max-width: none !important;
        margin-left: 0 !important;
    }
    
    /* Custom card styling - ensure full width */
    .custom-card {
        background: linear-gradient(135deg, #1E1E1E 0%, #262626 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #333;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        width: 100% !important;
        max-width: none !important;
        box-sizing: border-box;
    }
        max-width: none !important;
    }
    
    /* Status indicators */
    .status-success {
        background: linear-gradient(90deg, #00D4AA, #00A693);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.25rem;
        font-weight: 500;
    }
    
    .status-warning {
        background: linear-gradient(90deg, #FFA726, #FF8F00);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.25rem;
        font-weight: 500;
    }
    
    /* Modern metrics */
    .metric-card {
        background: linear-gradient(135deg, #2D2D2D 0%, #1A1A1A 100%);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #444;
        text-align: center;
        margin: 0.5rem 0;
        width: 100%;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #00D4AA;
        display: block;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #AAAAAA;
        margin-top: 0.25rem;
    }
    
    /* Citation styling */
    .citation-card {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
        border-left: 4px solid #00D4AA;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
    }
    
    /* Answer section - full width with explicit sizing */
    .answer-section {
        background: linear-gradient(135deg, #0F1419 0%, #1C1C1C 100%);
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #333;
        margin: 1rem 0;
        width: 100% !important;
        max-width: none !important;
        box-sizing: border-box;
    }
    
    /* Hide Streamlit style */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Custom sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #1E1E1E 0%, #0E1117 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #00D4AA, #0066CC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        color: #AAAAAA;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Force full width for all containers */
    .stColumn {
        width: 100% !important;
        max-width: none !important;
    }
    
    /* Column containers should use full width */
    div[data-testid="column"] {
        width: 100% !important;
        max-width: none !important;
    }
    
    /* Override any container width restrictions */
    div[data-testid="stVerticalBlock"] {
        width: 100% !important;
        max-width: none !important;
    }
    
    /* Additional Streamlit container overrides for newer versions */
    .stApp > div:first-child {
        width: 100% !important;
        max-width: none !important;
    }
    
    [data-testid="stAppViewContainer"] {
        width: 100% !important;
        max-width: none !important;
    }
    
    [data-testid="stHeader"] {
        width: 100% !important;
        max-width: none !important;
    }
    
    /* Force content area to full width */
    section.main > div {
        width: 100% !important;
        max-width: none !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    /* Ensure all text areas and inputs use full width */
    .stTextInput > div > div,
    .stTextArea > div > div,
    .stSelectbox > div > div {
        width: 100% !important;
    }
    
    /* Force answer and content sections to full width */
    div[data-testid="stMarkdownContainer"] {
        width: 100% !important;
        max-width: none !important;
    }
    
    /* Override Streamlit's responsive breakpoints */
    @media (min-width: 576px) {
        .main .block-container {
            max-width: none !important;
            width: 100% !important;
        }
    }
    
    @media (min-width: 768px) {
        .main .block-container {
            max-width: none !important;
            width: 100% !important;
        }
    }
    
    @media (min-width: 1024px) {
        .main .block-container {
            max-width: none !important;
            width: 100% !important;
        }
    }
    
    /* Target specific Streamlit containers that limit width */
    .css-1kyxreq,
    .css-12oz5g7,
    .css-1v0mbdj {
        max-width: none !important;
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# Import our custom modules
from document_processor import DocumentProcessor
from vector_store import VectorStore  
from reranker import RerankerService, FallbackReranker
from llm_service import LLMService


class RAGApp:
    """Main RAG Application Class"""
    
    def __init__(self):
        self.doc_processor = DocumentProcessor()
        self.vector_store = None
        self.reranker = None
        self.llm_service = None
        
        # Initialize services
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize all services with error handling"""
        try:
            self.vector_store = VectorStore()
            st.success("✅ Connected to Pinecone vector database")
        except Exception as e:
            st.error(f"❌ Failed to connect to Pinecone: {str(e)}")
            st.stop()
        
        try:
            self.reranker = RerankerService()
            st.success("✅ Connected to Cohere Reranker")
        except Exception as e:
            st.warning(f"⚠️ Cohere Reranker not available: {str(e)}. Using fallback reranker.")
            self.reranker = FallbackReranker()
        
        try:
            self.llm_service = LLMService()
            st.success("✅ Connected to Groq LLM")
        except Exception as e:
            st.error(f"❌ Failed to connect to Groq LLM: {str(e)}")
            st.stop()
    
    def run(self):
        """Main application runner with modern UI"""
        # Modern header
        st.markdown('<h1 class="main-header">🔍 RAG Demo</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Intelligent Document Q&A System with Advanced AI</p>', unsafe_allow_html=True)
        
        # Create main layout with modern cards - only show when no active query
        if 'query_results' not in st.session_state:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                # Status card
                self._render_status_card()
                
            with col2:
                # Quick stats card
                self._render_stats_card()
        
        # Sidebar for file upload and index management
        self._render_modern_sidebar()
        
        # Main content area
        self._render_modern_main_content()
    
    def _render_status_card(self):
        """Render modern status card"""
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("### 🔧 System Status")
        
        # Service status indicators
        services = [
            ("Pinecone Vector DB", self.vector_store is not None, "Connected"),
            ("Cohere Reranker", hasattr(self.reranker, 'co'), "Active"),
            ("Groq LLM", self.llm_service is not None, "Ready")
        ]
        
        for service, status, label in services:
            if status:
                st.markdown(f'<span class="status-success">✅ {service}: {label}</span>', unsafe_allow_html=True)
            else:
                st.markdown(f'<span class="status-warning">⚠️ {service}: Offline</span>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def _render_stats_card(self):
        """Render statistics card with metrics"""
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Knowledge Base Stats")
        
        stats = self.vector_store.get_index_stats()
        total_vectors = stats.get('total_vectors', 0)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <span class="metric-value">{total_vectors}</span>
                <div class="metric-label">Documents</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="metric-card">
                <span class="metric-value">768</span>
                <div class="metric-label">Dimensions</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            similarity_score = "Ready" if total_vectors > 0 else "Empty"
            st.markdown(f'''
            <div class="metric-card">
                <span class="metric-value" style="font-size: 1.2rem;">{similarity_score}</span>
                <div class="metric-label">Status</div>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def _render_modern_sidebar(self):
        """Render the modern sidebar with upload and management options"""
        with st.sidebar:
            st.markdown("## 📂 Document Management")
            
            # Modern file upload section
            st.markdown("### 📤 Upload Files")
            uploaded_files = st.file_uploader(
                "Choose documents",
                type=['pdf', 'txt'],
                accept_multiple_files=True,
                help="Upload PDF or TXT files to build your knowledge base",
                label_visibility="collapsed"
            )
            
            if uploaded_files:
                if st.button("� Process & Upload", type="primary", use_container_width=True):
                    self._process_and_upload_documents(uploaded_files)
            
            st.divider()
            
            # Modern text input section
            st.markdown("### ✍️ Direct Text Input")
            text_input = st.text_area(
                "Paste your content",
                height=150,
                placeholder="Paste your text content here for instant processing...",
                label_visibility="collapsed"
            )
            
            source_name = st.text_input(
                "📝 Source name",
                value="Pasted Text",
                help="Give a name to identify this text source"
            )
            
            if text_input and st.button("⚡ Process Text", type="primary", use_container_width=True):
                self._process_and_upload_text(text_input, source_name)
            
            st.divider()
            
            # Modern index management
            st.markdown("### 🗄️ Index Management")
            
            # Enhanced index stats
            stats = self.vector_store.get_index_stats()
            if 'error' not in stats:
                total_vectors = stats.get('total_vectors', 0)
                
                # Create a simple progress-like display
                if total_vectors > 0:
                    st.success(f"📊 **{total_vectors}** vectors indexed")
                    
                    # Storage estimation
                    storage_mb = (total_vectors * 768 * 4) / (1024 * 1024)  # 4 bytes per float
                    st.caption(f"📦 Estimated storage: {storage_mb:.2f} MB")
                else:
                    st.info("📊 Index is empty - upload documents to get started!")
            
            # Modern clear index button
            if st.button("🗑️ Clear All Data", type="secondary", use_container_width=True):
                if st.checkbox("⚠️ I understand this will delete all data", key="confirm_clear"):
                    with st.spinner("🧹 Clearing index..."):
                        if self.vector_store.clear_index():
                            st.success("✅ Index cleared successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to clear index")
    
    def _render_modern_main_content(self):
        """Render the modern main content area with Q&A interface"""
        # Check if we have any documents
        stats = self.vector_store.get_index_stats()
        if stats.get('total_vectors', 0) == 0:
            # Modern empty state
            st.markdown("""
            <div class="custom-card" style="text-align: center; padding: 3rem;">
                <h2>� Welcome to Your AI-Powered Q&A System</h2>
                <p style="font-size: 1.2rem; color: #AAAAAA; margin: 1rem 0;">
                    Upload documents or paste text in the sidebar to begin asking questions!
                </p>
                <div style="margin: 2rem 0;">
                    <span style="background: linear-gradient(90deg, #00D4AA, #0066CC); padding: 0.5rem 1rem; border-radius: 20px; color: white; font-weight: 500;">
                        👈 Start by uploading content
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            return
        
        # Modern query interface
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("## 💬 Ask Your Questions")
        
        # Enhanced query input
        query = st.text_input(
            "What would you like to know?",
            placeholder="e.g., 'What are the types of AI?' or 'How is machine learning used in healthcare?'",
            help="Ask any question about your uploaded documents",
            label_visibility="collapsed"
        )
        
        # Modern settings in columns
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Advanced settings in expander
            with st.expander("⚙️ Advanced Settings", expanded=False):
                settings_col1, settings_col2 = st.columns(2)
                with settings_col1:
                    top_k_retrieval = st.slider("📄 Documents to retrieve", 5, 50, 20, 
                                               help="More documents = better context, but slower processing")
                    top_k_rerank = st.slider("🎯 Documents to rerank", 3, 20, 5,
                                           help="Higher reranking = more accurate results")
                with settings_col2:
                    show_scores = st.checkbox("📊 Show similarity scores", value=False)
                    show_timing = st.checkbox("⏱️ Show performance metrics", value=True)
        
        with col2:
            if query:
                if st.button("🔍 Ask AI", type="primary", use_container_width=True):
                    self._process_query(query, top_k_retrieval, top_k_rerank, show_scores, show_timing)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Sample questions section
        if query == "":
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("### 💡 Try These Sample Questions")
            
            sample_questions = [
                "What is artificial intelligence?",
                "What are the types of AI?", 
                "How is AI used in healthcare?",
                "What is the difference between supervised and unsupervised learning?",
                "What are the main challenges facing AI implementation?"
            ]
            
            col1, col2 = st.columns(2)
            for i, question in enumerate(sample_questions):
                with col1 if i % 2 == 0 else col2:
                    if st.button(f"💭 {question}", key=f"sample_{i}", use_container_width=True):
                        st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    def _process_and_upload_documents(self, uploaded_files: List) -> None:
        """Process and upload multiple documents"""
        total_chunks = 0
        successful_files = 0
        
        progress_bar = st.sidebar.progress(0)
        status_text = st.sidebar.empty()
        
        for i, uploaded_file in enumerate(uploaded_files):
            try:
                status_text.text(f"Processing {uploaded_file.name}...")
                
                # Process document
                chunks = self.doc_processor.process_uploaded_file(uploaded_file)
                
                # Upload to vector store
                result = self.vector_store.upsert_documents(chunks)
                
                if result['success']:
                    total_chunks += result['upserted_count']
                    successful_files += 1
                    st.sidebar.success(f"✅ {uploaded_file.name}: {result['upserted_count']} chunks")
                else:
                    st.sidebar.error(f"❌ {uploaded_file.name}: {result['error']}")
                
                progress_bar.progress((i + 1) / len(uploaded_files))
                
            except Exception as e:
                st.sidebar.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
        
        status_text.text(f"✅ Complete! {successful_files}/{len(uploaded_files)} files processed successfully")
        st.sidebar.info(f"📊 Total chunks uploaded: {total_chunks}")
    
    def _process_and_upload_text(self, text: str, source_name: str) -> None:
        """Process and upload pasted text with enhanced metadata"""
        try:
            with st.spinner("Processing text..."):
                # Extract title from the text content
                title = self.doc_processor.extract_document_title(text, source_name)
                
                # Process text with title
                chunks = self.doc_processor.chunk_text(text, source_name, title)
                
                # Upload to vector store
                result = self.vector_store.upsert_documents(chunks)
                
                if result['success']:
                    st.sidebar.success(f"✅ {result['upserted_count']} chunks uploaded from '{source_name}'")
                    st.sidebar.info(f"📖 Title: {title}")
                else:
                    st.sidebar.error(f"❌ Error: {result['error']}")
                    
        except Exception as e:
            st.sidebar.error(f"❌ Error processing text: {str(e)}")
    
    def _process_query(self, query: str, top_k_retrieval: int, top_k_rerank: int, 
                      show_scores: bool, show_timing: bool) -> None:
        """Process user query and generate answer"""
        
        # Timing tracking
        start_time = time.time()
        timing_info = {}
        
        with st.spinner("🔍 Searching for relevant documents..."):
            # Step 1: Retrieve documents
            retrieval_start = time.time()
            try:
                retrieved_docs = self.vector_store.query_similar_documents(query, top_k_retrieval)
                timing_info['retrieval'] = time.time() - retrieval_start
                
                if not retrieved_docs:
                    st.warning("No relevant documents found for your query.")
                    return
                
            except Exception as e:
                st.error(f"Error during retrieval: {str(e)}")
                return
        
        with st.spinner("🎯 Reranking documents..."):
            # Step 2: Rerank documents
            rerank_start = time.time()
            try:
                reranked_docs = self.reranker.rerank_documents(query, retrieved_docs, top_k_rerank)
                timing_info['reranking'] = time.time() - rerank_start
            except Exception as e:
                st.error(f"Error during reranking: {str(e)}")
                return
        
        with st.spinner("🤖 Generating answer..."):
            # Step 3: Generate answer with LLM
            llm_start = time.time()
            try:
                result = self.llm_service.generate_answer_with_citations(query, reranked_docs)
                timing_info['llm_generation'] = time.time() - llm_start
                timing_info['total'] = time.time() - start_time
            except Exception as e:
                st.error(f"Error generating answer: {str(e)}")
                return
        
        # Display results
        self._display_results(result, reranked_docs, timing_info, show_scores, show_timing)
    
    def _display_results(self, result: Dict[str, Any], docs: List[Dict[str, Any]], 
                        timing_info: Dict[str, float], show_scores: bool, show_timing: bool):
        """Display the query results with modern styling and full width"""
        
        # Modern answer section - full width
        st.markdown('<div class="answer-section">', unsafe_allow_html=True)
        st.markdown("## 🤖 AI Response")
        st.markdown(result['answer'])
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Modern citations section - full width
        if result['citations']:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("## 📚 Source Citations")
            
            for citation in result['citations']:
                # Enhanced citation display
                citation_title = f"**[{citation['citation_num']}]** {citation['source']}"
                if citation.get('title'):
                    citation_title += f" - *{citation['title']}*"
                if citation.get('section'):
                    citation_title += f" → {citation['section']}"
                
                with st.expander(citation_title, expanded=False):
                    st.markdown(f"📝 **Content Preview:**")
                    st.markdown(f"> {citation['text_preview']}")
                    
                    # Enhanced metadata display - single line format
                    metadata_parts = []
                    if citation.get('section'):
                        metadata_parts.append(f"**📂 Section:** {citation['section']}")
                    if citation.get('position'):
                        metadata_parts.append(f"**📍 Position:** {citation['position']}")
                    if show_scores:
                        metadata_parts.append(f"**🎯 Score:** {citation['score']:.3f}")
                        if 'rerank_score' in citation:
                            metadata_parts.append(f"**⭐ Rerank:** {citation.get('rerank_score', 'N/A')}")
                    
                    if metadata_parts:
                        st.markdown(" | ".join(metadata_parts))
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Modern sources and performance in side-by-side layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Modern sources section
            if result['sources']:
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.markdown("## 📁 Document Sources")
                
                for source in result['sources']:
                    st.markdown(f'''
                    <div class="metric-card">
                        <span class="metric-value" style="font-size: 1.5rem;">{source['chunks_used']}</span>
                        <div class="metric-label">{source['source']}</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # Summary metrics
            if show_timing:
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.markdown("## ⚡ Quick Stats")
                
                metrics = [
                    ("⚡ Total Time", f"{timing_info.get('total', 0):.2f}s"),
                    ("🔍 Retrieved", f"{len(docs)} docs"),
                    ("🎯 Reranked", f"{len(result['citations'])} final"),
                    ("🤖 Tokens", f"{result.get('tokens_used', 0)}")
                ]
                
                for label, value in metrics:
                    st.markdown(f'''
                    <div class="metric-card">
                        <span class="metric-value" style="font-size: 1.2rem; color: #00D4AA;">{value}</span>
                        <div class="metric-label">{label}</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Modern performance chart - full width
        if show_timing:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("## 📊 Performance Analytics")
            
            # Create performance chart
            fig = go.Figure()
            
            stages = ['Retrieval', 'Reranking', 'Generation']
            times = [
                timing_info.get('retrieval', 0),
                timing_info.get('reranking', 0), 
                timing_info.get('llm_generation', 0)
            ]
            colors = ['#00D4AA', '#0066CC', '#FF6B6B']
            
            fig.add_trace(go.Bar(
                x=stages,
                y=times,
                marker_color=colors,
                text=[f"{t:.2f}s" for t in times],
                textposition='auto',
            ))
            
            fig.update_layout(
                title="Processing Time Breakdown",
                yaxis_title="Time (seconds)",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Debug information with modern styling
        if show_scores:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("## 🔍 Debug Information")
            
            for i, doc in enumerate(docs):
                with st.expander(f"**Document {i+1}:** {doc['source']} - {doc.get('section', 'Unknown')}", expanded=False):
                    st.markdown(f"**📝 Content:** {doc['text'][:200]}...")
                    if doc.get('title'):
                        st.markdown(f"**📖 Title:** {doc['title']}")
                    
                    # Debug metadata in single line
                    debug_parts = []
                    debug_parts.append(f"**🎯 Similarity:** {doc.get('score', 0):.3f}")
                    if 'rerank_score' in doc:
                        debug_parts.append(f"**⭐ Rerank:** {doc['rerank_score']:.3f}")
                    if doc.get('position'):
                        debug_parts.append(f"**📍 Position:** {doc['position']}")
                    
                    st.markdown(" | ".join(debug_parts))
            
            st.markdown('</div>', unsafe_allow_html=True)


def main():
    """Main function to run the Streamlit app"""
    app = RAGApp()
    app.run()


if __name__ == "__main__":
    main()
