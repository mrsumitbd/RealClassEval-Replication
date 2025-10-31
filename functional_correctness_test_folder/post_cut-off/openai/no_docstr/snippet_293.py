
import numpy as np


class KNNModel:
    def __init__(self, items, k=3):
        """
        Initialize the KNN model.

        Parameters
        ----------
        items : array-like
            A list or array of item embeddings. Each item should be an
            iterable of numeric values (e.g., list, tuple, or numpy array).
        k : int, optional
            The default number of nearest neighbors to return.
        """
        # Convert items to a 2D numpy array for efficient distance calculations.
        self.items = np.asarray(items, dtype=float)
        if self.items.ndim != 2:
            raise ValueError("`items` must be a 2D array-like structure.")
        self.k = int(k)

    def neighbors(self, target_emb, k=None):
        """
        Find the k nearest neighbors of a target embedding.

        Parameters
        ----------
        target_emb : array-like
            The embedding of the target item.
        k : int, optional
            The number of neighbors to return. If None, uses the default
            k specified at initialization.

        Returns
        -------
        list of tuples
            Each tuple contains (neighbor_embedding, distance) sorted by
            increasing distance.
        """
        if k is None:
            k = self.k
        else:
            k = int(k)

        if k <= 0:
            raise ValueError("`k` must be a positive integer.")

        target = np.asarray(target_emb, dtype=float)
        if target.ndim != 1:
            raise ValueError("`target_emb` must be a 1D array-like structure.")
        if target.shape[0] != self.items.shape[1]:
            raise ValueError(
                f"Dimension mismatch: target embedding has {target.shape[0]} "
                f"features, but items have {self.items.shape[1]} features."
            )

        # Compute Euclidean distances to all items.
        diffs = self.items - target
        dists = np.linalg.norm(diffs, axis=1)

        # Get indices of the k smallest distances.
        if k > len(self.items):
            k = len(self.items)
        nearest_idx = np.argpartition(dists, k - 1)[:k]
        # Sort the selected indices by actual distance.
        nearest_idx = nearest_idx[np.argsort(dists[nearest_idx])]

        # Return list of (embedding, distance) tuples.
        return [(self.items[i], dists[i]) for i in nearest_idx]
