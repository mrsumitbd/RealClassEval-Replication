
from typing import Any, Iterable, List, Sequence, Tuple
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
        self.k = k
        self.item_ids, embeddings = zip(*items)
        self.model = NearestNeighbors(metric='cosine', algorithm='brute')
        self.model.fit(embeddings)

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
        k = k if k is not None else self.k
        distances, indices = self.model.kneighbors([target_emb], n_neighbors=k)
        return [(self.item_ids[i], float(distances[0][j])) for j, i in enumerate(indices[0])]
