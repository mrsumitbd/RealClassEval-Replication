
import numpy as np


class RetrievalResult:

    def __init__(self, embedding: np.array, text: str, reference: str, metadata: dict, score: float = 0.0):
        self.embedding = embedding
        self.text = text
        self.reference = reference
        self.metadata = metadata
        self.score = score

    def __repr__(self):
        return (f"RetrievalResult("
                f"embedding=ndarray(shape={self.embedding.shape}, dtype={self.embedding.dtype}), "
                f"text={repr(self.text)}, "
                f"reference={repr(self.reference)}, "
                f"metadata={repr(self.metadata)}, "
                f"score={self.score})")
