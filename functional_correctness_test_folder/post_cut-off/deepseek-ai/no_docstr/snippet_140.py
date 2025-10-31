
from typing import Union, List
import numpy as np


class QwenEmbedding:

    def __init__(self, config=None):
        self.config = config if config is not None else {}
        self.embedding_dim = self.config.get('embedding_dim', 768)

    def embed(self, text: Union[str, List[str]]) -> List[List[float]]:
        if isinstance(text, str):
            return [np.random.rand(self.embedding_dim).tolist()]
        else:
            return [np.random.rand(self.embedding_dim).tolist() for _ in text]

    def encode(self, text: Union[str, List[str]]) -> List[List[float]]:
        return self.embed(text)

    def get_embedding_dim(self) -> int:
        return self.embedding_dim
