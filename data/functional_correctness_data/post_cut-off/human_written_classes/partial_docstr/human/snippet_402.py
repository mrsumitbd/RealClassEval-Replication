from typing import List, Dict, Any

class TokenAwareChunker:
    """Token-aware chunking implementation."""

    def __init__(self, chunk_size_tokens: int=400, chunk_overlap_tokens: int=75):
        self.chunk_size_chars = chunk_size_tokens * 4
        self.chunk_overlap_chars = chunk_overlap_tokens * 4

    def chunk_text(self, text: str) -> List[str]:
        """Chunk text with token awareness and overlap."""
        if not text or len(text) <= self.chunk_size_chars:
            return [text] if text else []
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + self.chunk_size_chars, len(text))
            if end < len(text):
                for separator in ['. ', '.\n', '! ', '? ', '\n\n', '\n', ' ']:
                    last_sep = text.rfind(separator, start, end)
                    if last_sep > start + self.chunk_size_chars // 2:
                        end = last_sep + len(separator)
                        break
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            if end >= len(text):
                break
            start = max(start + 1, end - self.chunk_overlap_chars)
        return chunks