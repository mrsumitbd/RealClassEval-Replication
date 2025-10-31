
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    metadata: Optional[dict] = None


class BaseEmbedding:

    def embed_query(self, text: str) -> List[float]:
        raise NotImplementedError("embed_query method must be implemented")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        raise NotImplementedError("embed_documents method must be implemented")

    def embed_chunks(self, chunks: List[Chunk], batch_size: int = 256) -> List[Chunk]:
        texts = [chunk.text for chunk in chunks]
        embeddings = self.embed_documents(texts)
        for chunk, embedding in zip(chunks, embeddings):
            chunk.metadata = chunk.metadata or {}
            chunk.metadata["embedding"] = embedding
        return chunks

    @property
    def dimension(self) -> int:
        raise NotImplementedError("dimension property must be implemented")
