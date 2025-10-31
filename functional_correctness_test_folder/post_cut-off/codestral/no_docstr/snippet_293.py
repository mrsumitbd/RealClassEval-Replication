
import numpy as np


class KNNModel:

    def __init__(self, items, k=3):
        self.items = items
        self.k = k

    def neighbors(self, target_emb, k=None):
        if k is None:
            k = self.k
        distances = np.linalg.norm(self.items - target_emb, axis=1)
        nearest_indices = np.argsort(distances)[:k]
        return self.items[nearest_indices]
