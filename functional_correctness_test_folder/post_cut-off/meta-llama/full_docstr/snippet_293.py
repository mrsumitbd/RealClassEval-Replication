
from sklearn.neighbors import NearestNeighbors
import numpy as np
from typing import Iterable, Tuple, Any, Sequence


class KNNModel:
    '''
    Thin wrapper around sklearn NearestNeighbors for cosine similarity retrieval.
    :ivar model: Fitted NearestNeighbors instance.
    :vartype model: NearestNeighbors
    :ivar k: Default number of neighbors.
    :vartype k: int
    '''

    def __init__(self, items, k=3):
        '''
        Initialize KNN index.
        :param items: Iterable of (item_id, embedding_vector) pairs.
        :type items: Iterable[Tuple[Any, Sequence[float]]]
        :param k: Default number of neighbors to retrieve.
        :type k: int
        '''
        item_ids, embeddings = zip(*items)
        self.item_ids = np.array(item_ids)
        self.embeddings = np.array(embeddings)
        self.model = NearestNeighbors(
            n_neighbors=k, metric='cosine', algorithm='brute').fit(self.embeddings)
        self.k = k

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
        k = k or self.k
        distances, indices = self.model.kneighbors([target_emb], n_neighbors=k)
        return list(zip(self.item_ids[indices[0]], distances[0]))
