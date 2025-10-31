
import numpy as np
from scipy.spatial import distance


class KNNModel:

    def __init__(self, items, k=3):
        self.items = items
        self.k = k

    def neighbors(self, target_emb, k=None):
        if k is None:
            k = self.k
        distances = [(i, distance.euclidean(target_emb, item))
                     for i, item in enumerate(self.items)]
        distances.sort(key=lambda x: x[1])
        return distances[:k]
