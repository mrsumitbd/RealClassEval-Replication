from __future__ import annotations

from typing import List


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
        if batch_size <= 0:
            raise ValueError('batch_size must be a positive integer.')

        # Extract texts, preferring `text`, then `content`.
        texts: List[str] = []
        for idx, ch in enumerate(chunks):
            text = getattr(ch, 'text', None)
            if text is None:
                text = getattr(ch, 'content', None)
            if text is None:
                raise ValueError(
                    f'Chunk at index {idx} is missing a text/content attribute.')
            texts.append(text)

        # Process in batches using embed_documents.
        for start in range(0, len(chunks), batch_size):
            end = min(start + batch_size, len(chunks))
            batch_texts = texts[start:end]
            embeddings = self.embed_documents(batch_texts)
            if len(embeddings) != len(batch_texts):
                raise ValueError(
                    'embed_documents returned a mismatched number of embeddings.')
            for offset, emb in enumerate(embeddings):
                ch = chunks[start + offset]
                if hasattr(ch, 'set_embedding') and callable(getattr(ch, 'set_embedding')):
                    ch.set_embedding(emb)  # type: ignore[attr-defined]
                else:
                    setattr(ch, 'embedding', emb)
        return chunks

    @property
    def dimension(self) -> int:
        '''
        Get the dimensionality of the embeddings.
        Returns:
            The number of dimensions in the embedding vectors.
        '''
        raise NotImplementedError(
            'dimension must be implemented by subclasses.')
