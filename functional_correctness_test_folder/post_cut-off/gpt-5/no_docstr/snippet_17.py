from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


class BaseEmbedding(ABC):
    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        raise NotImplementedError

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        raise NotImplementedError

    def embed_chunks(self, chunks: List[object], batch_size: int = 256) -> List[object]:
        if batch_size <= 0:
            raise ValueError("batch_size must be a positive integer")
        if not chunks:
            return chunks

        n = len(chunks)
        for start in range(0, n, batch_size):
            batch = chunks[start: start + batch_size]
            texts = []
            for c in batch:
                try:
                    text = getattr(c, "text")
                except AttributeError as e:
                    raise AttributeError(
                        "Each chunk must have a 'text' attribute") from e
                if not isinstance(text, str):
                    raise TypeError("Chunk.text must be a string")
                texts.append(text)
            embeddings = self.embed_documents(texts)
            if len(embeddings) != len(batch):
                raise ValueError(
                    "Number of embeddings does not match number of chunks in the batch")
            for c, emb in zip(batch, embeddings):
                try:
                    setattr(c, "embedding", emb)
                except Exception as e:
                    raise AttributeError(
                        "Each chunk must allow setting an 'embedding' attribute") from e
        return chunks

    @property
    @abstractmethod
    def dimension(self) -> int:
        raise NotImplementedError
