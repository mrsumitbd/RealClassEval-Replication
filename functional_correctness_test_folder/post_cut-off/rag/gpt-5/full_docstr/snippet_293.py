from typing import Any, Sequence, Iterable, Tuple, List, Optional
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
        pairs = list(items)
        if not pairs:
            raise ValueError(
                "items must be a non-empty iterable of (item_id, embedding_vector) pairs")

        self._ids: List[Any] = []
        vectors: List[Sequence[float]] = []
        for item_id, emb in pairs:
            self._ids.append(item_id)
            vectors.append(emb)

        X = np.asarray(vectors, dtype=float)
        if X.ndim != 2:
            raise ValueError(
                "Each embedding_vector must be a 1-D sequence of floats")
        self._emb_dim = X.shape[1]
        self._n_items = X.shape[0]

        if not isinstance(k, int) or k < 1:
            raise ValueError("k must be a positive integer")
        self.k = k

        self.model = NearestNeighbors(metric="cosine")
        self.model.fit(X)

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
        if self._n_items == 0:
            return []

        q = np.asarray(target_emb, dtype=float)
        if q.ndim != 1:
            raise ValueError("target_emb must be a 1-D sequence of floats")
        if q.shape[0] != self._emb_dim:
            raise ValueError(
                f"target_emb dimension {q.shape[0]} does not match index dimension {self._emb_dim}")

        n_neighbors = self.k if k is None else k
        if not isinstance(n_neighbors, int) or n_neighbors < 1:
            raise ValueError("k must be a positive integer")
        n_neighbors = min(n_neighbors, self._n_items)

        distances, indices = self.model.kneighbors(
            q.reshape(1, -1), n_neighbors=n_neighbors, return_distance=True)
        distances = distances[0]
        indices = indices[0]
        return [(self._ids[int(idx)], float(dist)) for idx, dist in zip(indices, distances)]
