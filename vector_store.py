"""
Vector database operations using Pinecone
"""
import time
from typing import List, Dict, Any, Optional
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from config import (
    PINECONE_API_KEY, 
    PINECONE_INDEX_NAME, 
    PINECONE_ENVIRONMENT,
    TOP_K_RETRIEVAL
)


class VectorStore:
    """Handles vector database operations with Pinecone"""
    
    def __init__(self):
        if not PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY not found in environment variables")
        
        # Initialize Pinecone
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index_name = PINECONE_INDEX_NAME
        
        # Initialize embedding model 
        self.embedding_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')  # 768 dimensions
        
        # Connect to existing index
        try:
            self.index = self.pc.Index(self.index_name)
        except Exception as e:
            raise Exception(f"Error connecting to Pinecone index '{self.index_name}': {str(e)}")
    
    def upsert_documents(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Upsert document chunks to Pinecone with embeddings
        """
        try:
            vectors_to_upsert = []
            
            for i, chunk in enumerate(chunks):
                vector_id = f"chunk_{int(time.time())}_{i}"
                
                # Generate embedding for the text
                text = chunk['text']
                embedding = self.embedding_model.encode(text).tolist()
                
                # Prepare metadata (Pinecone has limits on metadata size)
                metadata = {
                    'text': text[:8000],  # Limit text size for metadata
                    'source': chunk['metadata'].get('source', 'unknown'),
                    'title': chunk['metadata'].get('title', ''),
                    'section': chunk['metadata'].get('section', ''),
                    'position': chunk['metadata'].get('position', chunk['metadata'].get('chunk_index', 0)),
                    'chunk_index': chunk['metadata'].get('chunk_index', 0),
                    'chunk_size': chunk['metadata'].get('chunk_size', len(text))
                }
                
                # Standard Pinecone format with values
                vector_data = {
                    'id': vector_id,
                    'values': embedding,
                    'metadata': metadata
                }
                
                vectors_to_upsert.append(vector_data)
            
            # Upsert in batches
            batch_size = 100
            upserted_count = 0
            
            for i in range(0, len(vectors_to_upsert), batch_size):
                batch = vectors_to_upsert[i:i + batch_size]
                response = self.index.upsert(vectors=batch)
                upserted_count += len(batch)
                time.sleep(0.1)  # Rate limiting
            
            return {
                'success': True,
                'upserted_count': upserted_count,
                'total_chunks': len(chunks)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'upserted_count': 0,
                'total_chunks': len(chunks)
            }
    
    def query_similar_documents(self, query_text: str, top_k: int = None) -> List[Dict[str, Any]]:
        """
        Query Pinecone for similar documents using embeddings
        """
        if top_k is None:
            top_k = TOP_K_RETRIEVAL
        
        try:
            # Generate embedding for the query
            query_embedding = self.embedding_model.encode(query_text).tolist()
            
            # Query with embedding vector
            response = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            results = []
            for match in response['matches']:
                results.append({
                    'id': match['id'],
                    'score': match['score'],
                    'text': match['metadata'].get('text', ''),
                    'source': match['metadata'].get('source', 'unknown'),
                    'title': match['metadata'].get('title', ''),
                    'section': match['metadata'].get('section', ''),
                    'position': match['metadata'].get('position', 0),
                    'chunk_index': match['metadata'].get('chunk_index', 0)
                })
            
            return results
            
        except Exception as e:
            raise Exception(f"Error querying Pinecone: {str(e)}")
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the current index"""
        try:
            stats = self.index.describe_index_stats()
            return {
                'total_vectors': stats.get('total_vector_count', 0),
                'dimension': stats.get('dimension', 0),
                'index_fullness': stats.get('index_fullness', 0)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def clear_index(self) -> bool:
        """Clear all vectors from the index"""
        try:
            self.index.delete(delete_all=True)
            return True
        except Exception as e:
            print(f"Error clearing index: {str(e)}")
            return False
