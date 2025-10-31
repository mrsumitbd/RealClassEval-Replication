from typing import Dict, List, Optional, Any, Set, Tuple, Generator

class TokenAwareChunker:
    """Memory-efficient streaming chunker."""

    def __init__(self, chunk_size_tokens: int=400, chunk_overlap_tokens: int=75):
        self.chunk_size_chars = chunk_size_tokens * 4
        self.chunk_overlap_chars = chunk_overlap_tokens * 4
        logger.info(f'TokenAwareChunker: {chunk_size_tokens} tokens (~{self.chunk_size_chars} chars)')

    def chunk_text_stream(self, text: str) -> Generator[str, None, None]:
        """Stream chunks without holding all in memory."""
        if not text:
            return
        if len(text) <= self.chunk_size_chars:
            yield text
            return
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
                yield chunk
            if end >= len(text):
                break
            start = max(start + 1, end - self.chunk_overlap_chars)