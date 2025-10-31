from typing import Union, List, Optional, Dict, Any
import hashlib
import random
import math


class QwenEmbedding:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        cfg = config or {}
        self._dim = int(cfg.get("embedding_dim", cfg.get("dim", 1536)))
        self._normalize = bool(cfg.get("normalize", True))

    def _embed_one(self, text: str) -> List[float]:
        h = hashlib.sha256(text.encode("utf-8")).digest()
        seed = int.from_bytes(h, "big", signed=False)
        rng = random.Random(seed)
        vec = [(rng.random() - 0.5) for _ in range(self._dim)]
        if self._normalize:
            norm = math.sqrt(sum(v * v for v in vec)) or 1.0
            vec = [v / norm for v in vec]
        return vec

    def embed(self, text: Union[str, List[str]]) -> List[List[float]]:
        if isinstance(text, str):
            return [self._embed_one(text)]
        if isinstance(text, list):
            return [self._embed_one(t if isinstance(t, str) else str(t)) for t in text]
        raise TypeError("text must be a string or a list of strings")

    def encode(self, text: Union[str, List[str]]) -> List[List[float]]:
        return self.embed(text)

    def get_embedding_dim(self) -> int:
        return self._dim
