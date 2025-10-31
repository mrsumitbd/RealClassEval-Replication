
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
        ids: List[Any] = []
        vectors: List[Sequence[float]] = []

        for item_id, vec in items:
            ids.append(item_id)
            vectors.append(vec)

        if not vectors:
            raise ValueError("No items provided to build the KNN index.")

        # Convert to numpy array
        X = np.array(vectors, dtype=np.float32)

        # Build NearestNeighbors model with cosine metric
        self.model = NearestNeighbors(metric='cosine', algorithm='brute')
        self.model.fit(X)

        self.ids = ids
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
        # Ensure k does not exceed number of items
        k = min(k, len(self.ids))

        # Query the model
        distances, indices = self.model.kneighbors(
            [target_emb], n_neighbors=k, return_distance=True)

        # Flatten results
        distances = distances[0]
        indices = indices[0]

        # Build list of (id, distance) tuples
        result = [(self.ids[idx], float(distances[idx])) for idx in indices]
        return result
