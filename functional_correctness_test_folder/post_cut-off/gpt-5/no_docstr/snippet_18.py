import numpy as np


class RetrievalResult:

    def __init__(self, embedding: np.array, text: str, reference: str, metadata: dict, score: float = 0.0):
        self.embedding = None if embedding is None else np.asarray(embedding)
        self.text = "" if text is None else str(text)
        self.reference = "" if reference is None else str(reference)
        self.metadata = {} if metadata is None else dict(metadata)
        self.score = float(score)

    def __repr__(self):
        emb_shape = None if self.embedding is None else tuple(
            self.embedding.shape)
        text_preview = self.text if len(
            self.text) <= 60 else self.text[:57] + "..."
        meta_keys = list(self.metadata.keys())
        return (
            f"RetrievalResult(text={text_preview!r}, reference={self.reference!r}, "
            f"score={self.score:.6f}, embedding_shape={emb_shape}, metadata_keys={meta_keys})"
        )
