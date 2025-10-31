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
        self.embedding = embedding
        self.text = text
        self.reference = reference
        self.metadata = metadata
        self.score = score

    def __repr__(self):
        '''
        Return a string representation of the RetrievalResult.
        Returns:
            A string representation of the RetrievalResult object.
        '''
        emb_shape = None
        if isinstance(self.embedding, np.ndarray):
            emb_shape = self.embedding.shape
        else:
            emb_shape = str(type(self.embedding))
        return (f"RetrievalResult(embedding_shape={emb_shape}, "
                f"text={repr(self.text[:30] + '...' if len(self.text) > 30 else self.text)}, "
                f"reference={repr(self.reference)}, "
                f"metadata={repr(self.metadata)}, "
                f"score={self.score})")
