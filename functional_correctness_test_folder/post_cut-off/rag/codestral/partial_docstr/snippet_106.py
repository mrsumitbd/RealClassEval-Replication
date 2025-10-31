
import numpy as np
from typing import Any, Dict, List, Union
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
        self.embedding_model = embedding_model
        self.kwargs = kwargs

    def name(self) -> str:
        '''Return the name of the embedding model for ChromaDB compatibility.'''
        if isinstance(self.embedding_model, str):
            return self.embedding_model
        else:
            return self.embedding_model.__class__.__name__

    def __call__(self, input: Union[str, List[str]]) -> Union['np.ndarray', List['np.ndarray']]:
        '''Call the ChromaEmbeddingFunction.'''
        if isinstance(self.embedding_model, str):
            from langchain.embeddings import HuggingFaceEmbeddings
            embeddings = HuggingFaceEmbeddings(
                model_name=self.embedding_model, **self.kwargs)
        else:
            embeddings = self.embedding_model

        if isinstance(input, str):
            return np.array(embeddings.embed_query(input))
        else:
            return [np.array(embedding) for embedding in embeddings.embed_documents(input)]
