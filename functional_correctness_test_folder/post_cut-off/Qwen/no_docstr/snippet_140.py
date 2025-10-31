
from typing import Union, List


class QwenEmbedding:

    def __init__(self, config=None):
        self.config = config
        self.embedding_dim = 768  # Example dimension, can be adjusted based on actual model

    def embed(self, text: Union[str, List[str]]) -> List[List[float]]:
        # Dummy implementation for embedding
        if isinstance(text, str):
            text = [text]
        return [[0.0] * self.embedding_dim for _ in text]

    def encode(self, text: Union[str, List[str]]) -> List[List[float]]:
        # Dummy implementation for encoding
        return self.embed(text)

    def get_embedding_dim(self) -> int:
        return self.embedding_dim
