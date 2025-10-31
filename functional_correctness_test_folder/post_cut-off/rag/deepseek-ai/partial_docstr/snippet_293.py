
from sklearn.neighbors import NearestNeighbors
from typing import Any, Sequence, Tuple, List, Iterable


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
        self.k = k
        self._ids = []
        embeddings = []
        for item_id, emb in items:
            self._ids.append(item_id)
            embeddings.append(emb)
        self.model = NearestNeighbors(metric='cosine')
        self.model.fit(embeddings)

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
        if k is None:
            k = self.k
        distances, indices = self.model.kneighbors([target_emb], n_neighbors=k)
        return [(self._ids[i], distances[0][j]) for j, i in enumerate(indices[0])]
