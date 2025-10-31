from typing import Any, Iterable, List, Sequence, Tuple, Optional
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
        self.k = int(k)
        pairs = list(items)
        if not pairs:
            raise ValueError(
                "items must be a non-empty iterable of (item_id, embedding_vector) pairs.")

        self._ids: List[Any] = []
        vectors: List[np.ndarray] = []
        for item_id, emb in pairs:
            self._ids.append(item_id)
            vec = np.asarray(emb, dtype=float).ravel()
            vectors.append(vec)

        try:
            X = np.vstack(vectors)
        except ValueError as e:
            raise ValueError(
                "All embedding vectors must have the same dimension.") from e

        if X.ndim != 2 or X.shape[1] == 0:
            raise ValueError(
                "Embedding vectors must be non-empty 1-D sequences of equal length.")

        self.model = NearestNeighbors(metric='cosine', algorithm='brute')
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
        n = len(self._ids)
        if n == 0:
            return []

        k_eff = int(k) if k is not None else self.k
        if k_eff <= 0:
            return []

        k_eff = min(k_eff, n)
        q = np.asarray(target_emb, dtype=float).ravel().reshape(1, -1)
        distances, indices = self.model.kneighbors(
            q, n_neighbors=k_eff, return_distance=True)
        inds = indices[0]
        dists = distances[0]
        return [(self._ids[i], float(d)) for i, d in zip(inds, dists)]
