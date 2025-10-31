
from typing import Union, List, Dict, Any
import numpy as np
from langchain.embeddings import BaseEmbeddings


class ChromaEmbeddingFunction:

    def __init__(self, embedding_model: Union[str, BaseEmbeddings] = 'minishlab/potion-retrieval-32M', **kwargs: Dict[str, Any]) -> None:
        if isinstance(embedding_model, str):
            from langchain.embeddings import HuggingFaceEmbeddings
            self.embedding_model = HuggingFaceEmbeddings(
                model_name=embedding_model, **kwargs)
        else:
            self.embedding_model = embedding_model

    def name(self) -> str:
        return self.embedding_model.__class__.__name__

    def __call__(self, input: Union[str, List[str]]) -> Union[np.ndarray, List[np.ndarray]]:
        if isinstance(input, str):
            return np.array(self.embedding_model.embed_query(input))
        else:
            return [np.array(embedding) for embedding in self.embedding_model.embed_documents(input)]
