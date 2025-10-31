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
        self.embedding = np.asarray(embedding)
        self.text = '' if text is None else str(text)
        self.reference = '' if reference is None else str(reference)
        self.metadata = dict(metadata or {})
        self.score = float(score)

    def __repr__(self):
        '''
        Return a string representation of the RetrievalResult.
        Returns:
            A string representation of the RetrievalResult object.
        '''
        text_preview = self.text
        if len(text_preview) > 60:
            text_preview = text_preview[:57] + '...'
        return (
            f"RetrievalResult("
            f"embedding_shape={getattr(self.embedding, 'shape', None)}, "
            f"text={text_preview!r}, "
            f"reference={self.reference!r}, "
            f"score={self.score}, "
            f"metadata_keys={list(self.metadata.keys())})"
        )
