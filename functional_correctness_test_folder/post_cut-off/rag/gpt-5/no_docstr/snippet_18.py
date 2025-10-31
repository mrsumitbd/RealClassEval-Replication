import numpy as np
from typing import Optional, Dict, Any


class RetrievalResult:
    '''
    Represents a result retrieved from the vector database.
    This class encapsulates the information about a retrieved document,
    including its embedding, text content, reference, metadata, and similarity score.
    Attributes:
        embedding: The vector embedding of the document.
        text: The text content of the document.
        reference: A reference to the source of the document.
        metadata: Additional metadata associated with the document.
        score: The similarity score of the document to the query.
    '''

    def __init__(self, embedding: np.array, text: str, reference: str, metadata: dict, score: float = 0.0):
        '''
        Initialize a RetrievalResult object.
        Args:
            embedding: The vector embedding of the document.
            text: The text content of the document.
            reference: A reference to the source of the document.
            metadata: Additional metadata associated with the document.
            score: The similarity score of the document to the query. Defaults to 0.0.
        '''
        self.embedding = embedding if isinstance(
            embedding, np.ndarray) else np.asarray(embedding)
        self.text = '' if text is None else str(text)
        self.reference = '' if reference is None else str(reference)
        self.metadata = {} if metadata is None else dict(metadata)
        self.score = float(score)

    def __repr__(self):
        '''
        Return a string representation of the RetrievalResult.
        Returns:
            A string representation of the RetrievalResult object.
        '''
        text_preview = self.text
        if len(text_preview) > 48:
            text_preview = f"{text_preview[:47]}…"
        shape = getattr(self.embedding, 'shape', ())
        dtype = getattr(self.embedding, 'dtype', None)
        meta_keys = list(self.metadata.keys())
        return (f"RetrievalResult(embedding_shape={shape}, dtype={dtype}, "
                f"text={text_preview!r}, reference={self.reference!r}, "
                f"metadata_keys={meta_keys}, score={self.score})")
