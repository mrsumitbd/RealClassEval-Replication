
from typing import List


class Chunk:
    def __init__(self, text: str):
        self.text = text
        self.embedding = None


class BaseEmbedding:
    def __init__(self, dimension: int = 128):
        self._dimension = dimension

    def embed_query(self, text: str) -> List[float]:
        # Dummy embedding: hash-based deterministic vector
        return [(hash(text) + i) % 1000 / 1000.0 for i in range(self._dimension)]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_query(text) for text in texts]

    def embed_chunks(self, chunks: List[Chunk], batch_size: int = 256) -> List[Chunk]:
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            embeddings = self.embed_documents([chunk.text for chunk in batch])
            for chunk, emb in zip(batch, embeddings):
                chunk.embedding = emb
        return chunks

    @property
    def dimension(self) -> int:
        return self._dimension
