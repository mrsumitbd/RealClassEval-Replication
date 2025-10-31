
from typing import Sequence, Any, Tuple, List
import numpy as np
from scipy import spatial


class KNNModel:

    def __init__(self, items, k=3):
        self.items = items
        self.k = k
        self.embeddings = np.array([item['embedding'] for item in items])

    def neighbors(self, target_emb, k=None):
        if k is None:
            k = self.k
        distances = [spatial.distance.cosine(
            target_emb, emb) for emb in self.embeddings]
        indices = np.argsort(distances)[:k]
        return [(self.items[i]['id'], distances[i]) for i in indices]
