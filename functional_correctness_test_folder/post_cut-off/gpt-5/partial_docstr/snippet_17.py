from __future__ import annotations

from typing import List, Optional, Any


class BaseEmbedding:
    '''
    Abstract base class for embedding model implementations.
    This class defines the interface for embedding model implementations,
    including methods for embedding queries and documents, and a property
    for the dimensionality of the embeddings.
    '''

    def embed_query(self, text: str) -> List[float]:
        raise NotImplementedError(
            "embed_query must be implemented by subclasses.")

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
        return [self.embed_query(t) for t in texts]

    def embed_chunks(self, chunks: List['Chunk'], batch_size: int = 256) -> List['Chunk']:
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

        n = len(chunks)
        start = 0
        while start < n:
            end = min(start + batch_size, n)
            batch = chunks[start:end]

            texts: List[str] = [
                self._extract_text_from_chunk(c) for c in batch]
            embeddings = self.embed_documents(texts)

            if len(embeddings) != len(batch):
                raise ValueError(
                    "Number of embeddings does not match number of chunks in batch.")

            for chunk, emb in zip(batch, embeddings):
                setattr(chunk, "embedding", emb)

            start = end

        return chunks

    @property
    def dimension(self) -> int:
        '''
        Get the dimensionality of the embeddings.
        Returns:
            The number of dimensions in the embedding vectors.
        '''
        raise NotImplementedError(
            "dimension must be implemented by subclasses.")

    def _extract_text_from_chunk(self, chunk: Any) -> str:
        text_attrs = ("text", "content", "page_content", "document", "body")
        for attr in text_attrs:
            if hasattr(chunk, attr):
                value = getattr(chunk, attr)
                if isinstance(value, str):
                    return value
        # Fallback to string representation
        return str(chunk)
