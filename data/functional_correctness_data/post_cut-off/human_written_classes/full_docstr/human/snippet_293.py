from sklearn.neighbors import NearestNeighbors

class KNNModel:
    """
    Thin wrapper around sklearn NearestNeighbors for cosine similarity retrieval.

    :ivar model: Fitted NearestNeighbors instance.
    :vartype model: NearestNeighbors
    :ivar k: Default number of neighbors.
    :vartype k: int
    """

    def __init__(self, items, k=3):
        """
        Initialize KNN index.

        :param items: Iterable of (item_id, embedding_vector) pairs.
        :type items: Iterable[Tuple[Any, Sequence[float]]]
        :param k: Default number of neighbors to retrieve.
        :type k: int
        """
        self.model = NearestNeighbors(algorithm='auto', metric='cosine', n_jobs=-1)
        self.k = k
        self.model.ix2id = {ix: item for ix, (item, _) in enumerate(items)}
        self.model.fit([vec for _, vec in items])

    def neighbors(self, target_emb, k=None):
        """
        Retrieve k nearest neighbors by cosine distance.

        :param target_emb: Query embedding vector.
        :type target_emb: Sequence[float]
        :param k: Override number of neighbors (defaults to self.k).
        :type k: int
        :return: List of (item_id, distance) pairs ordered by proximity.
        :rtype: List[Tuple[Any, float]]
        """
        k = k or self.k
        dists, indexes = self.model.kneighbors([target_emb], min(k, len(self.model.ix2id)), return_distance=True)
        dists, indexes = (dists[0], indexes[0])
        return [(self.model.ix2id[indexes[ix]], dist) for ix, dist in enumerate(dists)]
    __call__ = neighbors