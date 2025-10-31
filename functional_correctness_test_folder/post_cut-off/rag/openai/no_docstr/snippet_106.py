
from typing import Any, Dict, List, Union
import numpy as np

# Import the base class for embeddings and a concrete implementation.
# These imports are optional; if the environment does not have langchain,
# the user must provide a compatible BaseEmbeddings instance.
try:
    from langchain.embeddings.base import BaseEmbeddings
    from langchain.embeddings.huggingface import HuggingFaceEmbeddings
except Exception:
    BaseEmbeddings = object  # type: ignore
    HuggingFaceEmbeddings = None  # type: ignore


class ChromaEmbeddingFunction:
    '''Chroma Embedding Function.
    Embeds the text of the chunks using the embedding model and 
    adds the embeddings to the chunks for use in downstream tasks
    like upserting into a vector database.
    Args:
        embedding_model: The embedding model to use.
        **kwargs: Additional keyword arguments.
    '''

    def __init__(
        self,
        embedding_model: Union[str,
                               BaseEmbeddings] = 'minishlab/potion-retrieval-32M',
        **kwargs: Dict[str, Any]
    ) -> None:
        '''Initialize the ChromaEmbeddingFunction.'''
        if isinstance(embedding_model, str):
            if HuggingFaceEmbeddings is None:
                raise ImportError(
                    "langchain is required to instantiate a HuggingFaceEmbeddings "
                    "model from a string name."
                )
            self.model = HuggingFaceEmbeddings(
                model_name=embedding_model, **kwargs
            )
            self._model_name = embedding_model
        else:
            # Assume a BaseEmbeddings instance is provided
            self.model = embedding_model
            # Try to get a name attribute; fall back to class name
            self._model_name = getattr(
                embedding_model, "model_name", embedding_model.__class__.__name__
            )

    def name(self) -> str:
        '''Return the name of the embedding model for ChromaDB compatibility.'''
        return self._model_name

    def __call__(
        self, input: Union[str, List[str]]
    ) -> Union[np.ndarray, List[np.ndarray]]:
        '''Call the ChromaEmbeddingFunction.'''
        if isinstance(input, str):
            # embed_query returns a list of floats
            vec = self.model.embed_query(input)
            return np.array(vec, dtype=np.float32)
        elif isinstance(input, list):
            # embed_documents returns a list of lists of floats
            vecs = self.model.embed_documents(input)
            return [np.array(v, dtype=np.float32) for v in vecs]
        else:
            raise TypeError(
                f"Unsupported input type {type(input)}. Expected str or List[str]."
            )
