
from typing import Union, List
import hashlib
import math


class QwenEmbedding:

    def __init__(self, config=None):
        if config is not None and isinstance(config, dict) and 'embedding_dim' in config:
            self.embedding_dim = int(config['embedding_dim'])
        else:
            self.embedding_dim = 384

    def _text_to_embedding(self, text: str) -> List[float]:
        # Deterministically hash the text to a vector of floats
        h = hashlib.sha256(text.encode('utf-8')).digest()
        floats = []
        for i in range(self.embedding_dim):
            idx = i % len(h)
            val = h[idx]
            # Map byte to float in [-1, 1]
            floats.append(math.sin(val + i) * 0.5 + 0.5)
        # Normalize
        norm = math.sqrt(sum(x*x for x in floats))
        if norm > 0:
            floats = [x / norm for x in floats]
        return floats

    def embed(self, text: Union[str, List[str]]) -> List[List[float]]:
        if isinstance(text, str):
            return [self._text_to_embedding(text)]
        elif isinstance(text, list):
            return [self._text_to_embedding(t) for t in text]
        else:
            raise TypeError("Input must be a string or list of strings.")

    def encode(self, text: Union[str, List[str]]) -> List[List[float]]:
        return self.embed(text)

    def get_embedding_dim(self) -> int:
        return self.embedding_dim
