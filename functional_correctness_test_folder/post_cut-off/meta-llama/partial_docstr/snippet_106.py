
import numpy as np
from typing import Union, List, Dict, Any
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

    def __init__(self, embedding_model: Union[str, BaseEmbeddings] = 'sentence-transformers/all-MiniLM-L6-v2', **kwargs: Dict[str, Any]) -> None:
        '''Initialize the ChromaEmbeddingFunction.'''
        if isinstance(embedding_model, str):
            self.embedding_model = HuggingFaceEmbeddings(
                model_name=embedding_model, **kwargs)
        else:
            self.embedding_model = embedding_model

    def name(self) -> str:
        '''Return the name of the embedding model for ChromaDB compatibility.'''
        if isinstance(self.embedding_model, HuggingFaceEmbeddings):
            return self.embedding_model.model_name
        else:
            return str(self.embedding_model)

    def __call__(self, input: Union[str, List[str]]) -> Union[np.ndarray, List[np.ndarray]]:
        if isinstance(input, str):
            return self.embedding_model.embed_query(input)
        else:
            return self.embedding_model.embed_documents(input)
