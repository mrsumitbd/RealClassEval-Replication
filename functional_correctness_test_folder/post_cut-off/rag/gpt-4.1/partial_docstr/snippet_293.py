from typing import Any, Sequence, Tuple, Iterable, List, Optional
from sklearn.neighbors import NearestNeighbors
import numpy as np


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
        self.k = k
        self._item_ids: List[Any] = []
        self._embeddings: List[List[float]] = []
        for item_id, emb in items:
            self._item_ids.append(item_id)
            self._embeddings.append(list(emb))
        self._embeddings_np = np.array(self._embeddings)
        self.model = NearestNeighbors(metric='cosine')
        if len(self._embeddings_np) > 0:
            self.model.fit(self._embeddings_np)
        else:
            self.model = None

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
        if self.model is None or len(self._item_ids) == 0:
            return []
        num_neighbors = k if k is not None else self.k
        num_neighbors = min(num_neighbors, len(self._item_ids))
        target_emb_np = np.array(target_emb).reshape(1, -1)
        distances, indices = self.model.kneighbors(
            target_emb_np, n_neighbors=num_neighbors)
        result = []
        for idx, dist in zip(indices[0], distances[0]):
            result.append((self._item_ids[idx], dist))
        return result
