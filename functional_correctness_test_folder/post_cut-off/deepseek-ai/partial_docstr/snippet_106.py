
import numpy as np
from typing import Union, List, Dict, Any
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
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(embedding_model)
            self._is_sentence_transformer = True
        elif isinstance(embedding_model, BaseEmbeddings):
            self.model = embedding_model
            self._is_sentence_transformer = False
        else:
            raise ValueError(
                "embedding_model must be a string or BaseEmbeddings instance")

    def name(self) -> str:
        '''Return the name of the embedding model for ChromaDB compatibility.'''
        if self._is_sentence_transformer:
            return self.model._model_name_or_path
        else:
            return self.model.__class__.__name__

    def __call__(self, input: Union[str, List[str]]) -> Union[np.ndarray, List[np.ndarray]]:
        if self._is_sentence_transformer:
            embeddings = self.model.encode(input) if isinstance(
                input, list) else self.model.encode([input])
            return embeddings[0] if isinstance(input, str) else embeddings
        else:
            embeddings = self.model.embed_documents(input) if isinstance(
                input, list) else self.model.embed_query(input)
            return np.array(embeddings[0]) if isinstance(input, str) else np.array(embeddings)
