from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class EmbeddingStoreItem:
    """嵌入库中的项"""

    def __init__(self, item_hash: str, embedding: List[float], content: str):
        self.hash = item_hash
        self.embedding = embedding
        self.str = content

    def to_dict(self) -> dict:
        """转为dict"""
        return {'hash': self.hash, 'embedding': self.embedding, 'str': self.str}