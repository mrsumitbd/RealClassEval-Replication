
from typing import List


class Chunk:
    def __init__(self, text: str, embedding: List[float] = None):
        self.text = text
        self.embedding = embedding


class BaseEmbedding:

    def embed_query(self, text: str) -> List[float]:
        # Placeholder implementation
        return [0.0] * self.dimension

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # Placeholder implementation
        return [[0.0] * self.dimension for _ in texts]

    def embed_chunks(self, chunks: List[Chunk], batch_size: int = 256) -> List[Chunk]:
        # Placeholder implementation
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            for chunk in batch:
                chunk.embedding = self.embed_query(chunk.text)
        return chunks

    @property
    def dimension(self) -> int:
        # Placeholder implementation
        return 128
