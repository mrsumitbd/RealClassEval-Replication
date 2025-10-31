
import math
from typing import Any, Iterable, List, Sequence, Tuple


class KNNModel:
    """
    A simple k‑Nearest Neighbours model that uses cosine distance.
    """

    def __init__(self, items: Iterable[Tuple[Any, Sequence[float]]], k: int = 3):
        """
        :param items: Iterable of (item_id, embedding) pairs.
        :param k: Default number of neighbours to return.
        """
        # Store items and pre‑compute norms for efficiency
        self.k = k
        self._items = []
        self._norms = {}
        for item_id, emb in items:
            norm = math.sqrt(sum(v * v for v in emb))
            self._items.append((item_id, emb))
            self._norms[item_id] = norm

    def neighbors(
        self, target_emb: Sequence[float], k: int | None = None
    ) -> List[Tuple[Any, float]]:
        """
        Retrieve k nearest neighbours by cosine distance.

        :param target_emb: Query embedding vector.
        :type target_emb: Sequence[float]
        :param k: Override number of neighbours (defaults to self.k).
        :type k: int
        :return: List of (item_id, distance) pairs ordered by proximity.
        :rtype: List[Tuple[Any, float]]
        """
        if k is None:
            k = self.k
        if k <= 0:
            return []

        target_norm = math.sqrt(sum(v * v for v in target_emb))
        if target_norm == 0:
            # All distances are undefined; return empty list
            return []

        distances: List[Tuple[Any, float]] = []
        for item_id, emb in self._items:
            # Compute cosine similarity
            dot = sum(a * b for a, b in zip(target_emb, emb))
            denom = target_norm * self._norms[item_id]
            if denom == 0:
                # Skip items with zero norm
                continue
            cos_sim = dot / denom
            # Cosine distance
            dist = 1.0 - cos_sim
            distances.append((item_id, dist))

        # Sort by distance (ascending) and return top k
        distances.sort(key=lambda x: x[1])
        return distances[:k]
