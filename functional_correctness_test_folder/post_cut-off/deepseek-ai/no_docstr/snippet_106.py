
import numpy as np
from typing import Union, List, Dict, Any
from langchain.embeddings.base import BaseEmbeddings


class ChromaEmbeddingFunction:

    def __init__(self, embedding_model: Union[str, BaseEmbeddings] = 'minishlab/potion-retrieval-32M', **kwargs: Dict[str, Any]) -> None:
        self.embedding_model = embedding_model
        if isinstance(embedding_model, str):
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(embedding_model, **kwargs)
        else:
            self.model = embedding_model

    def name(self) -> str:
        if isinstance(self.embedding_model, str):
            return self.embedding_model
        else:
            return self.embedding_model.__class__.__name__

    def __call__(self, input: Union[str, List[str]]) -> Union[np.ndarray, List[np.ndarray]]:
        if isinstance(self.embedding_model, str):
            embeddings = self.model.encode(input) if isinstance(
                input, str) else self.model.encode(input)
            return embeddings
        else:
            if isinstance(input, str):
                return np.array(self.model.embed_query(input))
            else:
                return np.array(self.model.embed_documents(input))
