from typing import List, Any, Iterable, Optional


class BaseEmbedding:
    '''
    Abstract base class for embedding model implementations.
    This class defines the interface for embedding model implementations,
    including methods for embedding queries and documents, and a property
    for the dimensionality of the embeddings.
    '''

    def embed_query(self, text: str) -> List[float]:
        '''
        Embed a single query text.
        Args:
            text: The query text to embed.
        Returns:
            A list of floats representing the embedding vector.
        '''
        raise NotImplementedError(
            'embed_query must be implemented by subclasses.')

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
        if texts is None:
            raise ValueError('texts must not be None')
        return [self.embed_query(text if text is not None else '') for text in texts]

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
        if chunks is None:
            raise ValueError('chunks must not be None')
        if batch_size is None or batch_size <= 0:
            batch_size = max(1, len(chunks))

        n = len(chunks)
        for start in range(0, n, batch_size):
            batch = chunks[start:start + batch_size]
            texts = [self._extract_text(chunk) for chunk in batch]
            embeddings = self.embed_documents(texts)
            if len(embeddings) != len(batch):
                raise ValueError(
                    'embed_documents returned a different number of embeddings than texts.')
            for chunk, emb in zip(batch, embeddings):
                self._set_embedding(chunk, emb)
        return chunks

    @staticmethod
    def _extract_text(chunk: Any) -> str:
        # Try common attribute names
        for attr in ('text', 'page_content', 'content', 'body'):
            if hasattr(chunk, attr):
                value = getattr(chunk, attr)
                if value is not None:
                    return str(value)
        # Try a getter method
        getter = getattr(chunk, 'get_text', None)
        if callable(getter):
            try:
                value = getter()
                if value is not None:
                    return str(value)
            except Exception:
                pass
        # Fallback to string representation
        return str(chunk)

    @staticmethod
    def _set_embedding(chunk: Any, embedding: List[float]) -> None:
        setter = getattr(chunk, 'set_embedding', None)
        if callable(setter):
            try:
                setter(embedding)
                return
            except Exception:
                pass
        # Try common attribute names
        for attr in ('embedding', 'vector', 'embedding_', 'emb'):
            try:
                setattr(chunk, attr, embedding)
                return
            except Exception:
                continue
        # Last resort: try updating a dict-like payload
        if hasattr(chunk, '__dict__'):
            try:
                setattr(chunk, 'embedding', embedding)
                return
            except Exception:
                pass
        # If we cannot set the embedding, silently ignore to keep method robust.

    @property
    def dimension(self) -> int:
        '''
        Get the dimensionality of the embeddings.
        Returns:
            The number of dimensions in the embedding vectors.
        '''
        raise NotImplementedError(
            'dimension must be implemented by subclasses.')
