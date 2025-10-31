
from typing import Union, List, Dict, Any
import numpy as np


class BaseEmbeddings:
    """Dummy base class for embedding models."""

    def embed(self, texts: List[str]) -> List[np.ndarray]:
        raise NotImplementedError

    @property
    def name(self) -> str:
        raise NotImplementedError


class DummyEmbeddingModel(BaseEmbeddings):
    """A dummy embedding model for demonstration."""

    def __init__(self, name: str):
        self._name = name

    def embed(self, texts: List[str]) -> List[np.ndarray]:
        # For demonstration, return random vectors
        return [np.random.rand(768).astype(np.float32) for _ in texts]

    @property
    def name(self) -> str:
        return self._name


class ChromaEmbeddingFunction:
    '''Chroma Embedding Function.
    Embeds the text of the chunks using the embedding model and 
    adds the embeddings to the chunks for use in downstream tasks
    like upserting into a vector database.
    Args:
        embedding_model: The embedding model to use.
        **kwargs: Additional keyword arguments.
    '''

    def __init__(self, embedding_model: Union[str, BaseEmbeddings] = 'minishlab/potion-retrieval-32M', **kwargs: Dict[str, Any]) -> None:
        '''Initialize the ChromaEmbeddingFunction.'''
        if isinstance(embedding_model, str):
            # In a real implementation, load the model by name
            self.embedding_model = DummyEmbeddingModel(embedding_model)
        else:
            self.embedding_model = embedding_model
        self.kwargs = kwargs

    def name(self) -> str:
        '''Return the name of the embedding model for ChromaDB compatibility.'''
        if hasattr(self.embedding_model, "name"):
            return self.embedding_model.name
        return str(self.embedding_model)

    def __call__(self, input: Union[str, List[str]]) -> Union['np.ndarray', List['np.ndarray']]:
        '''Call the ChromaEmbeddingFunction.'''
        if isinstance(input, str):
            embeddings = self.embedding_model.embed([input])
            return embeddings[0]
        elif isinstance(input, list):
            embeddings = self.embedding_model.embed(input)
            return embeddings
        else:
            raise TypeError("Input must be a string or a list of strings.")
