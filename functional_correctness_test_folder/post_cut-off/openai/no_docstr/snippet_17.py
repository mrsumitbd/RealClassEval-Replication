
from typing import List, Any
from abc import ABC, abstractmethod

Chunk = Any


class BaseEmbedding(ABC):
    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        """Return an embedding vector for a single query string."""
        pass

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Return a list of embedding vectors for a list of documents."""
        pass

    @abstractmethod
    def embed_chunks(self, chunks: List[Chunk], batch_size: int = 256) -> List[Chunk]:
        """Embed a list of chunks, optionally processing in batches."""
        pass

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Return the dimensionality of the embedding vectors."""
        pass
