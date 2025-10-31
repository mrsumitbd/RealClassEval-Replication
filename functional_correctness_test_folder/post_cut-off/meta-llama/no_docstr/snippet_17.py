
from typing import List


class Chunk:
    def __init__(self, text: str, embedding: List[float] = None):
        self.text = text
        self.embedding = embedding


class BaseEmbedding:

    def embed_query(self, text: str) -> List[float]:
        raise NotImplementedError("Subclass must implement abstract method")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_query(text) for text in texts]

    def embed_chunks(self, chunks: List[Chunk], batch_size: int = 256) -> List[Chunk]:
        texts = [chunk.text for chunk in chunks]
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_embeddings = self.embed_documents(batch_texts)
            embeddings.extend(batch_embeddings)
        for chunk, embedding in zip(chunks, embeddings):
            chunk.embedding = embedding
        return chunks

    @property
    def dimension(self) -> int:
        raise NotImplementedError("Subclass must implement abstract property")
