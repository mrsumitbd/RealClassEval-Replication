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
        if not isinstance(k, int) or k <= 0:
            raise ValueError("k must be a positive integer")

        ids: List[Any] = []
        vectors: List[Sequence[float]] = []

        for item_id, emb in items:
            ids.append(item_id)
            vectors.append(emb)

        if len(ids) == 0:
            raise ValueError(
                "items must contain at least one (item_id, embedding) pair")

        # Validate consistent dimensionality
        first_len = len(vectors[0])
        if any(len(v) != first_len for v in vectors):
            raise ValueError(
                "All embeddings must have the same dimensionality")

        X = np.asarray(vectors, dtype=np.float32)

        self.k: int = k
        self._ids: List[Any] = ids
        self._dim: int = first_len
        self._X = X

        self.model: NearestNeighbors = NearestNeighbors(metric="cosine")
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
        if k is None:
            k = self.k
        if not isinstance(k, int) or k <= 0:
            raise ValueError("k must be a positive integer")

        if len(self._ids) == 0:
            return []

        q = np.asarray(target_emb, dtype=np.float32)
        if q.ndim != 1 or q.shape[0] != self._dim:
            raise ValueError(
                f"target_emb must be a 1-D vector of length {self._dim}")

        k = min(k, len(self._ids))
        distances, indices = self.model.kneighbors(
            q.reshape(1, -1), n_neighbors=k, return_distance=True)
        dists = distances[0]
        inds = indices[0]

        return [(self._ids[idx], float(dist)) for dist, idx in zip(dists, inds)]
