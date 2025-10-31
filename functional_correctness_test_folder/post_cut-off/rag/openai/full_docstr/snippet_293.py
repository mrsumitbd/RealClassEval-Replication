
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
        # Separate ids and vectors
        self._ids: List[Any] = []
        vectors: List[List[float]] = []

        for item_id, vec in items:
            self._ids.append(item_id)
            vectors.append(list(vec))

        if not vectors:
            raise ValueError("No items provided to build the KNN index.")

        # Convert to numpy array
        X = np.array(vectors, dtype=np.float32)

        # Fit NearestNeighbors with cosine metric
        self.model = NearestNeighbors(
            # allow queries for any k <= len(items)
            n_neighbors=len(self._ids),
            metric='cosine',
            algorithm='brute'  # cosine with brute is fine for small to medium data
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
        if k <= 0:
            raise ValueError("k must be a positive integer.")
        k = min(k, len(self._ids))

        # Query the model
        distances, indices = self.model.kneighbors(
            np.array([list(target_emb)], dtype=np.float32),
            n_neighbors=k,
            return_distance=True
        )

        # Flatten results
        distances = distances[0]
        indices = indices[0]

        # Build list of (id, distance)
        result = [(self._ids[idx], float(dist))
                  for idx, dist in zip(indices, distances)]
        return result
