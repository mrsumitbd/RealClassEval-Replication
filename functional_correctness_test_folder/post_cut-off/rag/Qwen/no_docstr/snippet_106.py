
import numpy as np
from typing import Union, Dict, List, Any
from langchain.embeddings.base import BaseEmbeddings


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
            from langchain.embeddings import HuggingFaceEmbeddings
            self.embedding_model = HuggingFaceEmbeddings(
                model_name=embedding_model, **kwargs)
        elif isinstance(embedding_model, BaseEmbeddings):
            self.embedding_model = embedding_model
        else:
            raise ValueError(
                "embedding_model must be a string or an instance of BaseEmbeddings")

    def name(self) -> str:
        '''Return the name of the embedding model for ChromaDB compatibility.'''
        return self.embedding_model.model_name

    def __call__(self, input: Union[str, List[str]]) -> Union['np.ndarray', List['np.ndarray']]:
        '''Call the ChromaEmbeddingFunction.'''
        if isinstance(input, str):
            return np.array(self.embedding_model.embed_query(input))
        elif isinstance(input, list):
            return [np.array(embedding) for embedding in self.embedding_model.embed_documents(input)]
        else:
            raise ValueError("Input must be a string or a list of strings")
