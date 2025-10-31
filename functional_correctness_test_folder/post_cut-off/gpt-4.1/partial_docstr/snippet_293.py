
import numpy as np


class KNNModel:

    def __init__(self, items, k=3):
        """
        :param items: List of (item_id, embedding) pairs.
        :param k: Number of neighbors to retrieve by default.
        """
        self.k = k
        # items: list of (item_id, embedding)
        self.item_ids = []
        self.embeddings = []
        for item_id, emb in items:
            self.item_ids.append(item_id)
            self.embeddings.append(np.array(emb, dtype=np.float32))
        # shape: (n_items, emb_dim)
        self.embeddings = np.stack(self.embeddings, axis=0)
        # Precompute norms for cosine similarity
        self.norms = np.linalg.norm(self.embeddings, axis=1)

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
        target_emb = np.array(target_emb, dtype=np.float32)
        target_norm = np.linalg.norm(target_emb)
        if target_norm == 0:
            # All distances are undefined; return empty list
            return []
        # Compute cosine similarity
        dot_products = self.embeddings @ target_emb
        denom = self.norms * target_norm
        # To avoid division by zero
        denom = np.where(denom == 0, 1e-8, denom)
        cosine_sim = dot_products / denom
        # Cosine distance = 1 - cosine similarity
        cosine_dist = 1.0 - cosine_sim
        # Get indices of k smallest distances
        idxs = np.argsort(cosine_dist)[:k]
        result = []
        for idx in idxs:
            result.append((self.item_ids[idx], float(cosine_dist[idx])))
        return result
