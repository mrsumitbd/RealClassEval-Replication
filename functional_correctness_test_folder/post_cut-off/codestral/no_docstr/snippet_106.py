
import numpy as np
from typing import Union, List, Dict, Any
from langchain.embeddings.base import BaseEmbeddings


class ChromaEmbeddingFunction:

    def __init__(self, embedding_model: Union[str, BaseEmbeddings] = 'minishlab/potion-retrieval-32M', **kwargs: Dict[str, Any]) -> None:
        self.embedding_model = embedding_model
        self.kwargs = kwargs

    def name(self) -> str:
        if isinstance(self.embedding_model, str):
            return self.embedding_model
        else:
            return self.embedding_model.__class__.__name__

    def __call__(self, input: Union[str, List[str]]) -> Union['np.ndarray', List['np.ndarray']]:
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
