
import numpy as np


class KNNModel:

    def __init__(self, items, k=3):
        self.items = items
        self.k = k

    def neighbors(self, target_emb, k=None):
        if k is None:
            k = self.k
        distances = []
        for item in self.items:
            dist = np.linalg.norm(np.array(target_emb) - np.array(item))
            distances.append((item, dist))
        distances.sort(key=lambda x: x[1])
        return [item[0] for item in distances[:k]]
