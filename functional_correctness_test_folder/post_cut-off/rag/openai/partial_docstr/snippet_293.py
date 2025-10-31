
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
        # Separate ids and vectors
        ids, vectors = zip(*items) if items else ([], [])
        if not vectors:
            raise ValueError("No items provided to build the KNN index.")
        self.item_ids: List[Any] = list(ids)
        X = np.vstack([np.asarray(v, dtype=np.float32) for v in vectors])

        # Fit NearestNeighbors with cosine metric
        self.model = NearestNeighbors(
            n_neighbors=min(k, len(self.item_ids)),
            metric='cosine',
            algorithm='brute'
        )
        self.model.fit(X)
        self.k = k

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
        k = min(k, len(self.item_ids))
        if k == 0:
            return []

        X_query = np.asarray(target_emb, dtype=np.float32).reshape(1, -1)
        distances, indices = self.model.kneighbors(
            X_query, n_neighbors=k, return_distance=True)
        # distances and indices are 2D arrays with shape (1, k)
        result = [(self.item_ids[idx], float(dist))
                  for idx, dist in zip(indices[0], distances[0])]
        return result
