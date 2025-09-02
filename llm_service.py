"""
LLM service using Groq for generating answers with citations
"""
import re
from groq import Groq
from typing import List, Dict, Any, Tuple
from config import GROQ_API_KEY, LLM_MODEL, MAX_TOKENS, TEMPERATURE


class LLMService:
    """Handles LLM operations for generating answers with citations"""
    
    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        # Initialize Groq client with version compatibility
        try:
            self.client = Groq(api_key=GROQ_API_KEY)
        except TypeError as e:
            # Handle different Groq client versions
            if "proxies" in str(e):
                # Try without proxies parameter for older versions
                from groq import Client
                self.client = Client(api_key=GROQ_API_KEY)
            else:
                raise e
    
    def generate_answer_with_citations(self, query: str, context_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate an answer with inline citations using retrieved documents
        
        Args:
            query: User's question
            context_docs: List of relevant documents with text and metadata
        
        Returns:
            Dict with answer, citations, and metadata
        """
        if not context_docs:
            return {
                'answer': "I don't have enough relevant information to answer your question.",
                'citations': [],
                'sources': [],
                'tokens_used': 0
            }
        
        try:
            # Prepare context with citation markers
            context_text, citation_map = self._prepare_context_with_citations(context_docs)
            
            # Create the prompt
            prompt = self._create_rag_prompt(query, context_text)
            
            # Generate answer
            response = self.client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant that answers questions based on provided context. Always include citations in your answers using [1], [2], etc. format when referencing specific information from the context."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE
            )
            
            answer = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else 0
            
            # Extract and validate citations
            citations = self._extract_citations(answer, citation_map)
            
            # Prepare source information
            sources = self._prepare_sources(context_docs)
            
            return {
                'answer': answer,
                'citations': citations,
                'sources': sources,
                'tokens_used': tokens_used,
                'model_used': LLM_MODEL
            }
            
        except Exception as e:
            return {
                'answer': f"Error generating answer: {str(e)}",
                'citations': [],
                'sources': [],
                'tokens_used': 0
            }
    
    def _prepare_context_with_citations(self, docs: List[Dict[str, Any]]) -> Tuple[str, Dict[int, Dict]]:
        """Prepare context text with citation numbers and return citation map"""
        context_parts = []
        citation_map = {}
        
        for i, doc in enumerate(docs, 1):
            citation_num = i
            text = doc.get('text', '').strip()
            source = doc.get('source', 'Unknown')
            
            context_parts.append(f"[{citation_num}] {text}")
            
            citation_map[citation_num] = {
                'source': source,
                'title': doc.get('title', ''),
                'section': doc.get('section', ''),
                'position': doc.get('position', 0),
                'text': text[:200] + "..." if len(text) > 200 else text,
                'full_text': text,
                'chunk_index': doc.get('chunk_index', 0),
                'score': doc.get('score', 0),
                'rerank_score': doc.get('rerank_score', None)
            }
        
        context_text = "\n\n".join(context_parts)
        return context_text, citation_map
    
    def _create_rag_prompt(self, query: str, context: str) -> str:
        """Create the RAG prompt for the LLM"""
        prompt = f"""Based on the following context, please answer the question. Make sure to:
1. Use ONLY the information provided in the context
2. Include citations using [1], [2], etc. format when referencing specific information
3. If the context doesn't contain enough information to answer the question, say so clearly
4. Be concise but comprehensive in your answer

Context:
{context}

Question: {query}

Answer:"""
        return prompt
    
    def _extract_citations(self, answer: str, citation_map: Dict[int, Dict]) -> List[Dict[str, Any]]:
        """Extract citation numbers from answer and map to source information"""
        citation_pattern = r'\[(\d+)\]'
        cited_numbers = list(set(re.findall(citation_pattern, answer)))
        
        citations = []
        for num_str in cited_numbers:
            num = int(num_str)
            if num in citation_map:
                citation_info = citation_map[num]
                citations.append({
                    'citation_num': num,
                    'source': citation_info['source'],
                    'title': citation_info.get('title', ''),
                    'section': citation_info.get('section', ''),
                    'position': citation_info.get('position', 0),
                    'text_preview': citation_info['text'],
                    'score': citation_info['score']
                })
        
        # Sort by citation number
        citations.sort(key=lambda x: x['citation_num'])
        return citations
    
    def _prepare_sources(self, docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prepare source information for display"""
        sources = []
        seen_sources = set()
        
        for i, doc in enumerate(docs, 1):
            source = doc.get('source', 'Unknown')
            if source not in seen_sources:
                sources.append({
                    'citation_num': i,
                    'source': source,
                    'chunks_used': len([d for d in docs if d.get('source') == source])
                })
                seen_sources.add(source)
        
        return sources
    
    def handle_no_answer_case(self, query: str) -> Dict[str, Any]:
        """Handle cases where no relevant context is found"""
        return {
            'answer': "I don't have relevant information in my knowledge base to answer your question. Please try uploading relevant documents or rephrasing your question.",
            'citations': [],
            'sources': [],
            'tokens_used': 0
        }
