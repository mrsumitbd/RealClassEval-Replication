
import numpy as np
from typing import List, Tuple, Any, Sequence


class KNNModel:

    def __init__(self, items, k=3):
        self.items = items
        self.k = k

    def neighbors(self, target_emb, k=None):
        if k is None:
            k = self.k

        distances = []
        for item_id, item_emb in self.items:
            cosine_sim = np.dot(
                target_emb, item_emb) / (np.linalg.norm(target_emb) * np.linalg.norm(item_emb))
            cosine_dist = 1 - cosine_sim
            distances.append((item_id, cosine_dist))

        distances.sort(key=lambda x: x[1])
        return distances[:k]
