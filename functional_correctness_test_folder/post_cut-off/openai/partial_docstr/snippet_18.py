
import numpy as np


class RetrievalResult:
    def __init__(self, embedding: np.ndarray, text: str, reference: str, metadata: dict, score: float = 0.0):
        """
        Initialize a RetrievalResult instance.

        Parameters
        ----------
        embedding : np.ndarray
            The embedding vector associated with the retrieved text.
        text : str
            The retrieved text content.
        reference : str
            A reference identifier for the source of the text.
        metadata : dict
            Additional metadata related to the retrieval.
        score : float, optional
            Retrieval score (default is 0.0).
        """
        self.embedding = embedding
        self.text = text
        self.reference = reference
        self.metadata = metadata
        self.score = score

    def __repr__(self):
        """
        Return a string representation of the RetrievalResult.

        Returns
        -------
        str
            A string representation of the RetrievalResult object.
        """
        return (
            f"RetrievalResult(text={self.text!r}, "
            f"reference={self.reference!r}, "
            f"score={self.score}, "
            f"embedding_shape={self.embedding.shape}, "
            f"metadata={self.metadata})"
        )
