
import numpy as np


class KNNModel:

    def __init__(self, items, k=3):
        """
        Initialize the KNN model.

        Args:
        - items (list or numpy array): The list of items to be used for KNN search.
        - k (int, optional): The number of nearest neighbors to consider. Defaults to 3.
        """
        self.items = np.array(items)
        self.k = k

    def neighbors(self, target_emb, k=None):
        """
        Find the k nearest neighbors to the target embedding.

        Args:
        - target_emb (numpy array): The target embedding to find neighbors for.
        - k (int, optional): The number of nearest neighbors to consider. If not provided, uses the k value from the class initialization. Defaults to None.

        Returns:
        - neighbors (numpy array): The k nearest neighbors to the target embedding.
        - distances (numpy array): The distances between the target embedding and its k nearest neighbors.
        """
        if k is None:
            k = self.k

        # Calculate the distances between the target embedding and all items
        distances = np.linalg.norm(self.items - target_emb, axis=1)

        # Get the indices of the k nearest neighbors
        indices = np.argsort(distances)[:k]

        # Get the k nearest neighbors and their distances
        neighbors = self.items[indices]
        neighbor_distances = distances[indices]

        return neighbors, neighbor_distances


# Example usage:
if __name__ == "__main__":
    # Generate some random data
    np.random.seed(0)
    items = np.random.rand(10, 5)
    target_emb = np.random.rand(5)

    # Create a KNN model
    knn_model = KNNModel(items, k=3)

    # Find the 3 nearest neighbors to the target embedding
    neighbors, distances = knn_model.neighbors(target_emb)

    print("Neighbors:")
    print(neighbors)
    print("Distances:")
    print(distances)
