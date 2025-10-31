
import numpy as np
from collections import namedtuple
from typing import List, Tuple, Any, Sequence


class KNNModel:

    def __init__(self, items, k=3):
        self.items = items
        self.k = k

    def neighbors(self, target_emb: Sequence[float], k: int = None) -> List[Tuple[Any, float]]:
        if k is None:
            k = self.k

        def cosine_distance(a, b):
            a = np.array(a)
            b = np.array(b)
            dot_product = np.dot(a, b)
            norm_a = np.linalg.norm(a)
            norm_b = np.linalg.norm(b)
            return 1 - (dot_product / (norm_a * norm_b))

        distances = [(item_id, cosine_distance(target_emb, item_emb))
                     for item_id, item_emb in self.items]
        distances.sort(key=lambda x: x[1])
        return distances[:k]
