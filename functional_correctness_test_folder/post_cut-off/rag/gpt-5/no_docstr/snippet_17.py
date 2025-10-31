from typing import Any, List, Optional, Sequence
from abc import ABC, abstractmethod

# Define Chunk as typing alias to avoid NameError in annotations if not provided by the host application.
Chunk = Any


class BaseEmbedding(ABC):
    '''
    Abstract base class for embedding model implementations.
    This class defines the interface for embedding model implementations,
    including methods for embedding queries and documents, and a property
    for the dimensionality of the embeddings.
    '''

    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        '''
        Embed a single query text.
        Args:
            text: The query text to embed.
        Returns:
            A list of floats representing the embedding vector.
        '''
        raise NotImplementedError

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        '''
        Embed a list of document texts.
        This default implementation calls embed_query for each text,
        but implementations may override this with a more efficient batch method.
        Args:
            texts: A list of document texts to embed.
        Returns:
            A list of embedding vectors, one for each input text.
        '''
        if not texts:
            return []
        return [self.embed_query(text) for text in texts]

    def embed_chunks(self, chunks: List[Chunk], batch_size: int = 256) -> List[Chunk]:
        '''
        Embed a list of Chunk objects.
        This method extracts the text from each chunk, embeds it in batches,
        and updates the chunks with their embeddings.
        Args:
            chunks: A list of Chunk objects to embed.
            batch_size: The number of chunks to process in each batch.
        Returns:
            The input list of Chunk objects, updated with embeddings.
        '''
        if not chunks:
            return chunks

        def extract_text(chunk: Chunk) -> str:
            for attr in ('text', 'content', 'page_content'):
                if hasattr(chunk, attr):
                    value = getattr(chunk, attr)
                    return '' if value is None else str(value)
            if isinstance(chunk, str):
                return chunk
            raise AttributeError(
                "Chunk object has no 'text', 'content', or 'page_content' attribute.")

        n = len(chunks)
        for start in range(0, n, batch_size):
            batch = chunks[start:start + batch_size]
            texts = [extract_text(c) for c in batch]
            embeddings = self.embed_documents(texts)
            if len(embeddings) != len(batch):
                raise ValueError(
                    'Number of embeddings does not match number of chunks in the batch.')
            for c, emb in zip(batch, embeddings):
                setattr(c, 'embedding', emb)
        return chunks

    @property
    @abstractmethod
    def dimension(self) -> int:
        '''
        Get the dimensionality of the embeddings.
        Returns:
            The number of dimensions in the embedding vectors.
        '''
        raise NotImplementedError
