
from typing import Union, List, Dict, Any
import numpy as np


class BaseEmbeddings:
    def embed(self, texts: List[str]) -> List[np.ndarray]:
        raise NotImplementedError


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
            # Dummy embedding model for demonstration
            class DummyEmbeddingModel(BaseEmbeddings):
                def __init__(self, name):
                    self._name = name

                def embed(self, texts: List[str]) -> List[np.ndarray]:
                    # For demonstration, return random vectors
                    return [np.random.rand(768).astype(np.float32) for _ in texts]

                @property
                def name(self):
                    return self._name
            self.embedding_model = DummyEmbeddingModel(embedding_model)
        else:
            self.embedding_model = embedding_model
        self._name = getattr(self.embedding_model, 'name', None)
        if callable(self._name):
            self._name = self.embedding_model.name()
        elif self._name is None:
            self._name = str(type(self.embedding_model).__name__)

    def name(self) -> str:
        '''Return the name of the embedding model for ChromaDB compatibility.'''
        return self._name

    def __call__(self, input: Union[str, List[str]]) -> Union['np.ndarray', List['np.ndarray']]:
        if isinstance(input, str):
            embeddings = self.embedding_model.embed([input])
            return embeddings[0]
        elif isinstance(input, list):
            embeddings = self.embedding_model.embed(input)
            return embeddings
        else:
            raise TypeError("Input must be a string or a list of strings.")
