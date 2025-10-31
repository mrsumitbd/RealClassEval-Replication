from typing import Any, Iterable, Sequence, Tuple, List, Optional
import numpy as np
from sklearn.neighbors import NearestNeighbors


class KNNModel:
    '''
    Thin wrapper around sklearn NearestNeighbors for cosine similarity retrieval.
    :ivar model: Fitted NearestNeighbors instance.
    :vartype model: NearestNeighbors
    :ivar k: Default number of neighbors.
    :vartype k: int
    '''

    def __init__(self, items: Iterable[Tuple[Any, Sequence[float]]], k: int = 3):
        '''
        Initialize KNN index.
        :param items: Iterable of (item_id, embedding_vector) pairs.
        :type items: Iterable[Tuple[Any, Sequence[float]]]
        :param k: Default number of neighbors to retrieve.
        :type k: int
        '''
        if not isinstance(k, int) or k <= 0:
            raise ValueError("k must be a positive integer")

        ids: List[Any] = []
        embs: List[Sequence[float]] = []

        for item_id, emb in items:
            ids.append(item_id)
            embs.append(emb)

        if len(embs) == 0:
            raise ValueError(
                "items must contain at least one (item_id, embedding) pair")

        X = np.asarray(embs, dtype=float)
        if X.ndim != 2:
            raise ValueError(
                "Embeddings must be a 2D array-like of shape (n_items, n_dims)")

        self._ids: List[Any] = ids
        self._emb: np.ndarray = X
        self.k: int = k
        self.model: NearestNeighbors = NearestNeighbors(
            metric="cosine", algorithm="brute")
        self.model.fit(self._emb)

    def neighbors(self, target_emb: Sequence[float], k: Optional[int] = None) -> List[Tuple[Any, float]]:
        '''
        Retrieve k nearest neighbors by cosine distance.
        :param target_emb: Query embedding vector.
        :type target_emb: Sequence[float]
        :param k: Override number of neighbors (defaults to self.k).
        :type k: int
        :return: List of (item_id, distance) pairs ordered by proximity.
        :rtype: List[Tuple[Any, float]]
        '''
        k_val = self.k if k is None else k
        if not isinstance(k_val, int) or k_val <= 0:
            raise ValueError("k must be a positive integer")

        n_items = len(self._ids)
        k_query = min(k_val, n_items)

        q = np.asarray(target_emb, dtype=float).reshape(1, -1)
        distances, indices = self.model.kneighbors(
            q, n_neighbors=k_query, return_distance=True)
        dists = distances[0]
        idxs = indices[0]

        return [(self._ids[int(idx)], float(dist)) for dist, idx in zip(dists, idxs)]
