
from abc import ABC, abstractmethod
from typing import List, Any

# The Chunk type is expected to have at least `text` and `embedding` attributes.
# It is imported lazily to avoid circular dependencies.
try:
    from .chunk import Chunk  # type: ignore
except Exception:
    # Fallback: allow any object with the required attributes
    Chunk = Any


class BaseEmbedding(ABC):
    """
    Abstract base class for embedding model implementations.
    This class defines the interface for embedding model implementations,
    including methods for embedding queries and documents, and a property
    for the dimensionality of the embeddings.
    """

    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query text.
        Args:
            text: The query text to embed.
        Returns:
            A list of floats representing the embedding vector.
        """
        raise NotImplementedError

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of document texts.
        This default implementation calls embed_query for each text,
        but implementations may override this with a more efficient batch method.
        Args:
            texts: A list of document texts to embed.
        Returns:
            A list of embedding vectors, one for each input text.
        """
        return [self.embed_query(t) for t in texts]

    def embed_chunks(self, chunks: List[Chunk], batch_size: int = 256) -> List[Chunk]:
        """
        Embed a list of Chunk objects.
        This method extracts the text from each chunk, embeds it in batches,
        and updates the chunks with their embeddings.
        Args:
            chunks: A list of Chunk objects to embed.
            batch_size: The number of chunks to process in each batch.
        Returns:
            The input list of Chunk objects, updated with embeddings.
        """
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i: i + batch_size]
            texts = [c.text for c in batch]
            embeddings = self.embed_documents(texts)
            for c, emb in zip(batch, embeddings):
                c.embedding = emb
        return chunks

    @property
    @abstractmethod
    def dimension(self) -> int:
        """
        Get the dimensionality of the embeddings.
        Returns:
            The number of dimensions in the embedding vectors.
        """
        raise NotImplementedError
