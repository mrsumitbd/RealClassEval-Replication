from abc import ABC, abstractmethod
from typing import List, Optional, Protocol, runtime_checkable


@runtime_checkable
class Chunk(Protocol):
    text: str
    embedding: Optional[List[float]]


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
        return [self.embed_query(t) for t in texts]

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
        if batch_size <= 0:
            batch_size = 1

        def extract_text(ch: Chunk) -> str:
            txt = getattr(ch, "text", None)
            if isinstance(txt, str):
                return txt
            alt = getattr(ch, "content", None)
            if isinstance(alt, str):
                return alt
            # Fallback
            return str(ch)

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            texts = [extract_text(c) for c in batch]
            embeddings = self.embed_documents(texts)
            if len(embeddings) != len(batch):
                raise ValueError(
                    "embed_documents returned a mismatched number of embeddings.")
            for c, e in zip(batch, embeddings):
                try:
                    setattr(c, "embedding", e)
                except Exception as ex:
                    raise TypeError(
                        f"Failed to set embedding on chunk {c!r}: {ex}") from ex

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
