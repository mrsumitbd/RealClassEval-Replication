
from typing import Union, List, Dict, Any
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None


class BaseEmbeddings:
    def encode(self, input):
        raise NotImplementedError


class ChromaEmbeddingFunction:
    def __init__(self, embedding_model: Union[str, BaseEmbeddings] = 'minishlab/potion-retrieval-32M', **kwargs: Dict[str, Any]) -> None:
        self._model_name = None
        if isinstance(embedding_model, str):
            self._model_name = embedding_model
            if SentenceTransformer is None:
                raise ImportError(
                    "sentence-transformers is required for string embedding_model")
            self._model = SentenceTransformer(embedding_model, **kwargs)
        elif isinstance(embedding_model, BaseEmbeddings):
            self._model = embedding_model
            self._model_name = getattr(
                embedding_model, 'name', lambda: embedding_model.__class__.__name__)()
        else:
            raise ValueError(
                "embedding_model must be a string or BaseEmbeddings instance")

    def name(self) -> str:
        return self._model_name

    def __call__(self, input: Union[str, List[str]]) -> Union['np.ndarray', List['np.ndarray']]:
        if isinstance(input, str):
            emb = self._model.encode([input])
            return np.array(emb[0])
        elif isinstance(input, list):
            emb = self._model.encode(input)
            return [np.array(e) for e in emb]
        else:
            raise ValueError("Input must be a string or list of strings")
