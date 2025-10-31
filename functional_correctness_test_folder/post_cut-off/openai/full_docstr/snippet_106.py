
from typing import Union, Dict, Any, List
import numpy as np
from langchain.embeddings.base import BaseEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings


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
            self.embedding_model = HuggingFaceEmbeddings(
                model_name=embedding_model, **kwargs
            )
        else:
            self.embedding_model = embedding_model

    def name(self) -> str:
        '''Return the name of the embedding model for ChromaDB compatibility.'''
        if isinstance(self.embedding_model, HuggingFaceEmbeddings):
            return self.embedding_model.model_name
        # Fallback to the class name if no explicit model name is available
        return type(self.embedding_model).__name__

    def __call__(
        self, input: Union[str, List[str]]
    ) -> Union[np.ndarray, List[np.ndarray]]:
        '''Call the ChromaEmbeddingFunction.'''
        if isinstance(input, str):
            # Single string: embed_query returns a list of floats
            vec = self.embedding_model.embed_query(input)
            return np.array(vec, dtype=np.float32)
        elif isinstance(input, list):
            # List of strings: embed_documents returns list of lists
            vecs = self.embedding_model.embed_documents(input)
            return [np.array(v, dtype=np.float32) for v in vecs]
        else:
            raise TypeError(
                f"Unsupported input type {type(input)}. Expected str or List[str]."
            )
