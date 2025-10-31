
from abc import ABC, abstractmethod
from typing import List, Iterable

# A minimal Chunk definition for type checking.
# In real usage, this should be replaced with the actual Chunk class.


class Chunk:
    def __init__(self, text: str):
        self.text = text
        self.embedding = None


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
        Embed a single query string.
        Must be implemented by subclasses.
        """
        pass

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
        # Extract texts in order
        texts = [chunk.text for chunk in chunks]
        # Process in batches
        for start in range(0, len(texts), batch_size):
            end = start + batch_size
            batch_texts = texts[start:end]
            batch_embeddings = self.embed_documents(batch_texts)
            # Assign embeddings back to chunks
            for i, embedding in enumerate(batch_embeddings):
                chunks[start + i].embedding = embedding
        return chunks

    @property
    @abstractmethod
    def dimension(self) -> int:
        """
        Get the dimensionality of the embeddings.
        Must be implemented by subclasses.
        Returns:
            The number of dimensions in the embedding vectors.
        """
        pass
