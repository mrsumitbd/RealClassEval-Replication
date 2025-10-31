
import numpy as np


class KNNModel:

    def __init__(self, items, k=3):
        # items: list of (id, embedding) pairs
        self.items = items
        self.k = k
        self.ids = [item[0] for item in items]
        self.embeddings = np.array([item[1] for item in items])

    def neighbors(self, target_emb, k=None):
        if k is None:
            k = self.k
        target_emb = np.array(target_emb)
        # Compute Euclidean distances
        dists = np.linalg.norm(self.embeddings - target_emb, axis=1)
        idxs = np.argsort(dists)[:k]
        return [(self.ids[i], dists[i]) for i in idxs]
