
import numpy as np


class RetrievalResult:

    def __init__(self, embedding: np.array, text: str, reference: str, metadata: dict, score: float = 0.0):
        self.embedding = embedding
        self.text = text
        self.reference = reference
        self.metadata = metadata
        self.score = score

    def __repr__(self):
        emb_shape = self.embedding.shape if isinstance(
            self.embedding, np.ndarray) else None
        return (f"RetrievalResult(embedding_shape={emb_shape}, "
                f"text={repr(self.text)}, reference={repr(self.reference)}, "
                f"metadata={repr(self.metadata)}, score={self.score})")
