from typing import Any, Dict, List, Union
import numpy as np

try:
    from langchain.embeddings.base import BaseEmbeddings
except ImportError:
    BaseEmbeddings = object


class ChromaEmbeddingFunction:
    '''Chroma Embedding Function.
    Embeds the text of the chunks using the embedding model and 
    adds the embeddings to the chunks for use in downstream tasks
    like upserting into a vector database.
    Args:
        embedding_model: The embedding model to use.
        **kwargs: Additional keyword arguments.
    '''

    def __init__(self, embedding_model: Union[str, 'BaseEmbeddings'] = 'minishlab/potion-retrieval-32M', **kwargs: Dict[str, Any]) -> None:
        '''Initialize the ChromaEmbeddingFunction.'''
        if isinstance(embedding_model, str):
            # Try to import HuggingFaceEmbeddings from langchain if available
            try:
                from langchain_community.embeddings import HuggingFaceEmbeddings
            except ImportError:
                try:
                    from langchain.embeddings import HuggingFaceEmbeddings
                except ImportError:
                    raise ImportError(
                        "HuggingFaceEmbeddings not found. Please install langchain or langchain_community.")
            self.embedding_model = HuggingFaceEmbeddings(
                model_name=embedding_model, **kwargs)
            self._model_name = embedding_model
        else:
            self.embedding_model = embedding_model
            self._model_name = getattr(
                embedding_model, "model_name", embedding_model.__class__.__name__)

    def name(self) -> str:
        '''Return the name of the embedding model for ChromaDB compatibility.'''
        return str(self._model_name)

    def __call__(self, input: Union[str, List[str]]) -> Union['np.ndarray', List['np.ndarray']]:
        '''Call the ChromaEmbeddingFunction.'''
        if isinstance(input, str):
            emb = self.embedding_model.embed_query(input)
            return np.array(emb)
        elif isinstance(input, list):
            emb_list = self.embedding_model.embed_documents(input)
            return [np.array(e) for e in emb_list]
        else:
            raise TypeError("Input must be a string or a list of strings.")
