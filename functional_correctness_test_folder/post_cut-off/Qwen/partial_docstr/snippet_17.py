
from typing import List


class Chunk:
    def __init__(self, text: str, embedding: List[float] = None):
        self.text = text
        self.embedding = embedding


class ConcreteEmbedding(BaseEmbedding):
    def __init__(self, dimension: int):
        self._dimension = dimension

    def embed_query(self, text: str) -> List[float]:
        # Dummy implementation for embedding a single query
        return [0.0] * self._dimension

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # Default implementation calls embed_query for each text
        return [self.embed_query(text) for text in texts]

    def embed_chunks(self, chunks: List[Chunk], batch_size: int = 256) -> List[Chunk]:
        # Extract texts from chunks
        texts = [chunk.text for chunk in chunks]
        # Embed texts in batches
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_embeddings = self.embed_documents(batch_texts)
            for chunk, embedding in zip(chunks[i:i + batch_size], batch_embeddings):
                chunk.embedding = embedding
        return chunks

    @property
    def dimension(self) -> int:
        return self._dimension
