"""
Document processing utilities for chunking and text extraction
"""
import re
import PyPDF2
from typing import List, Dict, Any
from io import BytesIO
from config import CHUNK_SIZE, CHUNK_OVERLAP


class DocumentProcessor:
    """Handles document processing, text extraction, and chunking"""
    
    def __init__(self):
        pass
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text from uploaded PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def extract_text_from_txt(self, txt_file) -> str:
        """Extract text from uploaded text file"""
        try:
            return txt_file.read().decode('utf-8')
        except Exception as e:
            raise Exception(f"Error reading text file: {str(e)}")
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
        return text.strip()
    
    def extract_document_title(self, text: str, source_name: str) -> str:
        """Extract or derive document title from text or filename"""
        # Try to find title in first few lines
        lines = text.split('\n')[:5]
        for line in lines:
            line = line.strip()
            if line and len(line) < 100 and not line.startswith('#'):
                # Check if it looks like a title (not too long, meaningful)
                if any(word.istitle() for word in line.split()[:3]):
                    return line
        
        # Fallback to filename without extension
        return source_name.rsplit('.', 1)[0] if '.' in source_name else source_name
    
    def detect_sections(self, text: str) -> List[Dict[str, Any]]:
        """Detect sections in the document based on headers and structure"""
        sections = []
        lines = text.split('\n')
        current_section = "Introduction"
        position = 0
        
        # Common section patterns
        section_patterns = [
            r'^#{1,6}\s+(.+)$',  # Markdown headers
            r'^([A-Z][A-Za-z\s]+):?\s*$',  # Capitalized lines
            r'^\d+\.\s+(.+)$',  # Numbered sections
            r'^[A-Z\s]{3,}$',  # ALL CAPS sections
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*$'  # Title Case
        ]
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            # Check if line matches section pattern
            for pattern in section_patterns:
                match = re.match(pattern, line)
                if match and len(line) < 100:  # Reasonable title length
                    # Extract section name
                    if match.groups():
                        current_section = match.group(1).strip()
                    else:
                        current_section = line.strip()
                    break
            
            sections.append({
                'text': line,
                'section': current_section,
                'position': position
            })
            position += len(line) + 1  # +1 for newline
        
        return sections
    
    def chunk_text(self, text: str, source_name: str = "unknown", title: str = None) -> List[Dict[str, Any]]:
        """
        Split text into overlapping chunks with enhanced metadata
        """
        clean_text = self.clean_text(text)
        
        # Extract title if not provided
        if title is None:
            title = self.extract_document_title(clean_text, source_name)
        
        # Detect sections in the document
        sections_data = self.detect_sections(clean_text)
        
        # Create a mapping of text positions to sections
        position_to_section = {}
        current_pos = 0
        for section_info in sections_data:
            position_to_section[current_pos] = section_info['section']
            current_pos += len(section_info['text']) + 1
        
        # Simple sentence-aware chunking
        sentences = re.split(r'(?<=[.!?])\s+', clean_text)
        
        chunks = []
        current_chunk = ""
        chunk_index = 0
        chunk_start_position = 0
        
        for sentence in sentences:
            # If adding this sentence would exceed chunk size, save current chunk
            if len(current_chunk) + len(sentence) > CHUNK_SIZE and current_chunk:
                # Find the section for this chunk based on its position
                chunk_section = self._find_section_for_position(chunk_start_position, position_to_section)
                
                chunks.append({
                    'text': current_chunk.strip(),
                    'metadata': {
                        'source': source_name,
                        'title': title,
                        'section': chunk_section,
                        'position': chunk_start_position,
                        'chunk_index': chunk_index,
                        'chunk_size': len(current_chunk.strip())
                    }
                })
                
                # Start new chunk with overlap
                overlap_text = current_chunk[-CHUNK_OVERLAP:] if len(current_chunk) > CHUNK_OVERLAP else current_chunk
                chunk_start_position += len(current_chunk) - len(overlap_text)
                current_chunk = overlap_text + " " + sentence
                chunk_index += 1
            else:
                if not current_chunk:
                    chunk_start_position = len(clean_text) - len(' '.join(sentences[sentences.index(sentence):]))
                current_chunk += " " + sentence if current_chunk else sentence
        
        # Add the last chunk if it has content
        if current_chunk.strip():
            chunk_section = self._find_section_for_position(chunk_start_position, position_to_section)
            chunks.append({
                'text': current_chunk.strip(),
                'metadata': {
                    'source': source_name,
                    'title': title,
                    'section': chunk_section,
                    'position': chunk_start_position,
                    'chunk_index': chunk_index,
                    'chunk_size': len(current_chunk.strip())
                }
            })
        
        return chunks
    
    def _find_section_for_position(self, position: int, position_to_section: Dict[int, str]) -> str:
        """Find the appropriate section for a given text position"""
        # Find the closest section position that's less than or equal to our position
        best_section = "Unknown"
        best_pos = -1
        
        for pos, section in position_to_section.items():
            if pos <= position and pos > best_pos:
                best_pos = pos
                best_section = section
        
        return best_section
    
    def process_uploaded_file(self, uploaded_file) -> List[Dict[str, Any]]:
        """Process uploaded file and return chunks with enhanced metadata"""
        file_name = uploaded_file.name
        
        if file_name.lower().endswith('.pdf'):
            text = self.extract_text_from_pdf(uploaded_file)
        elif file_name.lower().endswith('.txt'):
            text = self.extract_text_from_txt(uploaded_file)
        else:
            raise ValueError("Unsupported file type. Please upload PDF or TXT files.")
        
        if not text.strip():
            raise ValueError("No text content found in the uploaded file.")
        
        # Extract title from document content
        title = self.extract_document_title(text, file_name)
        
        return self.chunk_text(text, source_name=file_name, title=title)
