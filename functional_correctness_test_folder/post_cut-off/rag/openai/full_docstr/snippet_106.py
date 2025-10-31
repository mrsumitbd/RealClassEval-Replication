
import numpy as np
from typing import Any, Dict, List, Union

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
            # Instantiate a HuggingFaceEmbeddings model
            self.embedding_model = HuggingFaceEmbeddings(
                model_name=embedding_model, **kwargs
            )
        else:
            self.embedding_model = embedding_model

    def name(self) -> str:
        '''Return the name of the embedding model for ChromaDB compatibility.'''
        if isinstance(self.embedding_model, str):
            return self.embedding_model
        # Try common attributes that may hold the model name
        for attr in ('model_name', 'model', 'name'):
            if hasattr(self.embedding_model, attr):
                return getattr(self.embedding_model, attr)
        return str(self.embedding_model)

    def __call__(
        self, input: Union[str, List[str]]
    ) -> Union['np.ndarray', List['np.ndarray']]:
        '''Call the ChromaEmbeddingFunction.'''
        if isinstance(input, str):
            # Single string: embed as a query
            vec = self.embedding_model.embed_query(input)
            return np.array(vec, dtype=np.float32)
        else:
            # List of strings: embed as documents
            if not input:
                return []
            vecs = self.embedding_model.embed_documents(input)
            return [np.array(v, dtype=np.float32) for v in vecs]
