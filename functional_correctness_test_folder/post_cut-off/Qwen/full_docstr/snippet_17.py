
from typing import List


class Chunk:
    def __init__(self, text: str, embedding: List[float] = None):
        self.text = text
        self.embedding = embedding


class ConcreteEmbedding(BaseEmbedding):
    def __init__(self, dimension: int):
        self._dimension = dimension

    def embed_query(self, text: str) -> List[float]:
        # Dummy implementation for demonstration
        return [0.0] * self._dimension

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_query(text) for text in texts]

    def embed_chunks(self, chunks: List[Chunk], batch_size: int = 256) -> List[Chunk]:
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            embeddings = self.embed_documents([chunk.text for chunk in batch])
            for chunk, embedding in zip(batch, embeddings):
                chunk.embedding = embedding
        return chunks

    @property
    def dimension(self) -> int:
        return self._dimension
