
from typing import Any, Iterable, List, Sequence, Tuple
from sklearn.neighbors import NearestNeighbors
import numpy as np


class KNNModel:
    """Thin wrapper around sklearn NearestNeighbors for cosine similarity retrieval.

    :ivar model: Fitted NearestNeighbors instance.
    :vartype model: NearestNeighbors
    :ivar k: Default number of neighbors.
    :vartype k: int
    """

    def __init__(self, items: Iterable[Tuple[Any, Sequence[float]]], k: int = 3):
        """
        Initialize KNN index.

        :param items: Iterable of (item_id, embedding_vector) pairs.
        :type items: Iterable[Tuple[Any, Sequence[float]]]
        :param k: Default number of neighbors to retrieve.
        :type k: int
        """
        item_ids, embeddings = zip(*items)
        self.item_ids = np.array(item_ids)
        embeddings = np.array(embeddings)

        # Normalize the embeddings to unit vectors for cosine similarity
        embeddings = embeddings / \
            np.linalg.norm(embeddings, axis=1, keepdims=True)

        self.model = NearestNeighbors(
            n_neighbors=k, metric='cosine', algorithm='brute')
        self.model.fit(embeddings)
        self.k = k

    def neighbors(self, target_emb: Sequence[float], k: int = None) -> List[Tuple[Any, float]]:
        """
        Retrieve k nearest neighbors by cosine distance.

        :param target_emb: Query embedding vector.
        :type target_emb: Sequence[float]
        :param k: Override number of neighbors (defaults to self.k).
        :type k: int
        :return: List of (item_id, distance) pairs ordered by proximity.
        :rtype: List[Tuple[Any, float]]
        """
        if k is None:
            k = self.k

        # Normalize the target embedding to a unit vector for cosine similarity
        target_emb = np.array(target_emb) / np.linalg.norm(target_emb)

        # Reshape to (1, -1) to represent a single sample
        target_emb = target_emb.reshape(1, -1)

        distances, indices = self.model.kneighbors(target_emb, n_neighbors=k)
        distances = distances.flatten()
        indices = indices.flatten()

        # Get the corresponding item ids
        neighbor_ids = self.item_ids[indices]

        return list(zip(neighbor_ids, distances))
