
import numpy as np


class RetrievalResult:

    def __init__(self, embedding: np.array, text: str, reference: str, metadata: dict, score: float = 0.0):
        self.embedding = embedding
        self.text = text
        self.reference = reference
        self.metadata = metadata
        self.score = score

    def __repr__(self):
        return (f"RetrievalResult(embedding={self.embedding}, text='{self.text}', "
                f"reference='{self.reference}', metadata={self.metadata}, score={self.score})")
