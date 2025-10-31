
from typing import Union, Dict, Any, List
import numpy as np

# Import the base class for embeddings
try:
    from langchain.embeddings.base import BaseEmbeddings
except Exception:
    # Fallback if langchain is not installed
    BaseEmbeddings = object  # type: ignore

# Import a concrete embeddings implementation
try:
    from langchain.embeddings.huggingface import HuggingFaceEmbeddings
except Exception:
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
                    "langchain.embeddings.huggingface is not available. "
                    "Install langchain to use string model names."
                )
            self.embedding_model = HuggingFaceEmbeddings(
                model_name=embedding_model, **kwargs
            )
        else:
            # Assume it's already a BaseEmbeddings instance
            self.embedding_model = embedding_model
        self.kwargs = kwargs

    def name(self) -> str:
        '''Return the name of the embedding model for ChromaDB compatibility.'''
        # Try to get a readable name from the embedding model
        if hasattr(self.embedding_model, "model_name"):
            return getattr(self.embedding_model, "model_name")
        if hasattr(self.embedding_model, "model"):
            return getattr(self.embedding_model, "model")
        # Fallback to the class name
        return self.embedding_model.__class__.__name__

    def __call__(self, input: Union[str, List[str]]) -> Union[np.ndarray, List[np.ndarray]]:
        '''Embed the input text(s) and return numpy arrays.'''
        if isinstance(input, str):
            # Single string: use embed_query
            vec = self.embedding_model.embed_query(input)
            return np.array(vec, dtype=np.float32)
        elif isinstance(input, list):
            # List of strings: use embed_documents
            vecs = self.embedding_model.embed_documents(input)
            return [np.array(v, dtype=np.float32) for v in vecs]
        else:
            raise TypeError(
                f"Unsupported input type {type(input)}. "
                "Expected str or List[str]."
            )
