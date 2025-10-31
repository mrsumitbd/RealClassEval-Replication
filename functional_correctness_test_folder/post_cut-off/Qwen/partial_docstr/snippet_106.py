
from typing import Union, List, Dict, Any
from abc import ABC, abstractmethod
import numpy as np


class BaseEmbeddings(ABC):
    @abstractmethod
    def embed(self, input: Union[str, List[str]]) -> Union[np.ndarray, List[np.ndarray]]:
        pass


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
            # Here you would typically load the model based on the string
            # For the sake of this example, we'll just store the string
            self.embedding_model = embedding_model
        elif isinstance(embedding_model, BaseEmbeddings):
            self.embedding_model = embedding_model
        else:
            raise ValueError(
                "embedding_model must be a string or an instance of BaseEmbeddings")
        self.kwargs = kwargs

    def name(self) -> str:
        '''Return the name of the embedding model for ChromaDB compatibility.'''
        return self.embedding_model if isinstance(self.embedding_model, str) else self.embedding_model.__class__.__name__

    def __call__(self, input: Union[str, List[str]]) -> Union[np.ndarray, List[np.ndarray]]:
        if isinstance(self.embedding_model, str):
            # Placeholder for actual embedding logic
            # Here you would use the string to call the appropriate embedding function
            # For the sake of this example, we'll just return a dummy numpy array
            if isinstance(input, str):
                return np.random.rand(32)  # Example embedding size
            else:
                # Example embedding size
                return [np.random.rand(32) for _ in input]
        else:
            return self.embedding_model.embed(input)
