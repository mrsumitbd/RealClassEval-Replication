
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

    def __init__(self, embedding: np.ndarray, text: str, reference: str, metadata: dict, score: float = 0.0):
        '''
        Initialize a RetrievalResult object.
        Args:
            embedding: The vector embedding of the document.
            text: The text content of the document.
            reference: A reference to the source of the document.
            metadata: Additional metadata associated with the document.
            score: The similarity score of the document to the query. Defaults to 0.0.
        '''
        if not isinstance(embedding, np.ndarray):
            raise TypeError(
                f"embedding must be a numpy.ndarray, got {type(embedding).__name__}")
        if not isinstance(text, str):
            raise TypeError(f"text must be a str, got {type(text).__name__}")
        if not isinstance(reference, str):
            raise TypeError(
                f"reference must be a str, got {type(reference).__name__}")
        if not isinstance(metadata, dict):
            raise TypeError(
                f"metadata must be a dict, got {type(metadata).__name__}")
        if not isinstance(score, (float, int)):
            raise TypeError(
                f"score must be a float, got {type(score).__name__}")

        self.embedding = embedding
        self.text = text
        self.reference = reference
        self.metadata = metadata
        self.score = float(score)

    def __repr__(self):
        '''
        Return a string representation of the RetrievalResult.
        Returns:
            A string representation of the RetrievalResult object.
        '''
        return (
            f"RetrievalResult(embedding_shape={self.embedding.shape}, "
            f"text_length={len(self.text)}, "
            f"reference={self.reference!r}, "
            f"metadata_keys={list(self.metadata.keys())}, "
            f"score={self.score:.4f})"
        )
