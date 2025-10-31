import numpy as np
from typing import Any, Dict, Optional


class RetrievalResult:

    def __init__(self, embedding: Optional[np.ndarray], text: str, reference: str, metadata: Dict[str, Any], score: float = 0.0):
        self.embedding = None if embedding is None else np.asarray(embedding)
        self.text = str(text)
        self.reference = str(reference)
        self.metadata = dict(metadata) if metadata is not None else {}
        self.score = float(score)

    def __repr__(self):
        '''
        Return a string representation of the RetrievalResult.
        Returns:
            A string representation of the RetrievalResult object.
        '''
        emb_shape = self.embedding.shape if isinstance(
            self.embedding, np.ndarray) else None
        emb_dtype = self.embedding.dtype if isinstance(
            self.embedding, np.ndarray) else None
        meta_keys = list(self.metadata.keys()) if isinstance(
            self.metadata, dict) else None
        return (
            f"RetrievalResult("
            f"text={self.text!r}, "
            f"reference={self.reference!r}, "
            f"score={self.score!r}, "
            f"embedding_shape={emb_shape}, "
            f"embedding_dtype={emb_dtype}, "
            f"metadata_keys={meta_keys})"
        )
