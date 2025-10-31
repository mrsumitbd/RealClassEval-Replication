
import numpy as np
from sklearn.neighbors import NearestNeighbors
from typing import Any, Iterable, Sequence, Tuple, List


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
        # Separate ids and embeddings
        ids = []
        vectors = []
        for item_id, vec in items:
            ids.append(item_id)
            vectors.append(vec)

        if not vectors:
            raise ValueError("No items provided to build the KNN index.")

        self.ids = np.array(ids)
        X = np.vstack(vectors)

        # Fit NearestNeighbors with cosine distance
        self.model = NearestNeighbors(
            n_neighbors=min(k, len(ids)),
            metric='cosine',
            algorithm='auto',
            n_jobs=-1
        )
        self.model.fit(X)

        self.k = k

    def neighbors(self, target_emb: Sequence[float], k: int = None) -> List[Tuple[Any, float]]:
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
        if k > len(self.ids):
            k = len(self.ids)

        target_arr = np.array(target_emb).reshape(1, -1)
        distances, indices = self.model.kneighbors(
            target_arr, n_neighbors=k, return_distance=True)

        # distances and indices are 2D arrays with shape (1, k)
        result = []
        for dist, idx in zip(distances[0], indices[0]):
            result.append((self.ids[idx], float(dist)))
        return result
