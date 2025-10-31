
import numpy as np


class RetrievalResult:
    """
    Represents a single retrieval result with its embedding, text, reference, metadata, and similarity score.
    """

    def __init__(self, embedding: np.ndarray, text: str, reference: str, metadata: dict, score: float = 0.0):
        """
        Initialize a RetrievalResult instance.

        Parameters
        ----------
        embedding : np.ndarray
            The embedding vector associated with the result.
        text : str
            The retrieved text snippet.
        reference : str
            A reference identifier (e.g., document ID or URL).
        metadata : dict
            Additional metadata about the result.
        score : float, optional
            Similarity or relevance score (default is 0.0).
        """
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

    def __repr__(self) -> str:
        """
        Return an unambiguous string representation of the object.
        """
        # Show only the first few elements of the embedding for brevity
        embed_preview = (
            f"{self.embedding[:5]}{'...' if self.embedding.size > 5 else ''}"
        )
        return (
            f"RetrievalResult("
            f"text={self.text!r}, "
            f"reference={self.reference!r}, "
            f"score={self.score:.4f}, "
            f"embedding={embed_preview}, "
            f"metadata={self.metadata!r}"
            f")"
        )
