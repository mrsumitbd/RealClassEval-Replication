import numpy as np


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
        if embedding is None:
            raise ValueError("embedding must not be None")
        arr = np.asarray(embedding)
        if arr.ndim > 1:
            arr = arr.reshape(-1)
        self.embedding = arr

        if not isinstance(text, str):
            raise TypeError("text must be a string")
        self.text = text

        if not isinstance(reference, str):
            raise TypeError("reference must be a string")
        self.reference = reference

        if metadata is None:
            metadata = {}
        if not isinstance(metadata, dict):
            raise TypeError("metadata must be a dict")
        self.metadata = dict(metadata)

        try:
            self.score = float(score)
        except (TypeError, ValueError):
            raise TypeError(
                "score must be a float-convertible value") from None

    def __repr__(self):
        '''
        Return a string representation of the RetrievalResult.
        Returns:
            A string representation of the RetrievalResult object.
        '''
        text_preview = self.text if len(
            self.text) <= 50 else self.text[:47] + "..."
        meta_keys = list(self.metadata.keys())
        return (
            f"RetrievalResult(reference={self.reference!r}, "
            f"score={self.score:.4f}, "
            f"text_preview={text_preview!r}, "
            f"embedding_shape={self.embedding.shape}, "
            f"metadata_keys={meta_keys})"
        )
