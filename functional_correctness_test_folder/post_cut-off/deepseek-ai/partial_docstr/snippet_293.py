
import numpy as np
from typing import Sequence, Any, Tuple, List


class KNNModel:

    def __init__(self, items, k=3):
        self.items = items
        self.k = k

    def neighbors(self, target_emb, k=None):
        '''
        Retrieve k nearest neighbors by cosine distance.
        :param target_emb: Query embedding vector.
        :type target_emb: Sequence[float]
        :param k: Override number of neighbors (defaults to self.k).
        :type k: int
        :return: List of (item_id, distance) pairs ordered by proximity.
        :rtype: List[Tuple[Any, float]]
        '''
        if k is None:
            k = self.k

        target_emb = np.array(target_emb)
        distances = []

        for item_id, emb in self.items:
            emb = np.array(emb)
            cosine_sim = np.dot(target_emb, emb) / \
                (np.linalg.norm(target_emb) * np.linalg.norm(emb))
            cosine_dist = 1 - cosine_sim
            distances.append((item_id, cosine_dist))

        distances.sort(key=lambda x: x[1])
        return distances[:k]
