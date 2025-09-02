"""
Reranking service using Cohere Rerank API
"""
import cohere
from typing import List, Dict, Any
from config import COHERE_API_KEY, TOP_K_RERANK


class RerankerService:
    """Handles document reranking using Cohere Rerank API"""
    
    def __init__(self):
        if not COHERE_API_KEY:
            raise ValueError("COHERE_API_KEY not found in environment variables")
        
        self.co = cohere.Client(COHERE_API_KEY)
    
    def rerank_documents(self, query: str, documents: List[Dict[str, Any]], top_k: int = None) -> List[Dict[str, Any]]:
        """
        Rerank documents using Cohere Rerank API
        
        Args:
            query: The search query
            documents: List of documents with 'text' field
            top_k: Number of top documents to return
        
        Returns:
            List of reranked documents with updated scores
        """
        if top_k is None:
            top_k = TOP_K_RERANK
        
        if not documents:
            return []
        
        try:
            # Extract text content for reranking
            doc_texts = [doc['text'] for doc in documents]
            
            # Call Cohere Rerank API
            rerank_response = self.co.rerank(
                model="rerank-english-v3.0",
                query=query,
                documents=doc_texts,
                top_n=min(top_k, len(documents)),
                return_documents=True
            )
            
            # Reconstruct documents with new ranking
            reranked_docs = []
            for result in rerank_response.results:
                original_doc = documents[result.index]
                reranked_doc = original_doc.copy()
                reranked_doc['rerank_score'] = result.relevance_score
                reranked_doc['original_rank'] = result.index
                reranked_docs.append(reranked_doc)
            
            return reranked_docs
            
        except Exception as e:
            # Fallback: return original documents if reranking fails
            print(f"Reranking failed: {str(e)}. Returning original order.")
            return documents[:top_k] if top_k else documents


class FallbackReranker:
    """Simple fallback reranker that just returns top documents by similarity score"""
    
    def rerank_documents(self, query: str, documents: List[Dict[str, Any]], top_k: int = None) -> List[Dict[str, Any]]:
        """
        Simple fallback reranking by similarity score
        """
        if top_k is None:
            top_k = TOP_K_RERANK
        
        # Sort by similarity score (descending) and return top_k
        sorted_docs = sorted(documents, key=lambda x: x.get('score', 0), reverse=True)
        return sorted_docs[:top_k]
