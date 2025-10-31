from scipy.sparse import coo_matrix, issparse
import numpy as np

class FastNeighbors:
    """TODO."""

    def __init__(self, n_neighbors=30, num_threads=-1):
        self.n_neighbors = n_neighbors
        self.num_threads = num_threads
        self.knn_indices, self.knn_distances = (None, None)
        self.distances, self.connectivities = (None, None)

    def fit(self, X, metric='l2', M=16, ef=100, ef_construction=100, random_state=0):
        """TODO."""
        try:
            import hnswlib
        except ImportError:
            print('In order to use fast approx neighbor search, you need to `pip install hnswlib`\n')
        ef_c, ef = (max(ef_construction, self.n_neighbors), max(self.n_neighbors, ef))
        metric = 'l2' if metric == 'euclidean' else metric
        X = X.toarray() if issparse(X) else X
        ns, dim = X.shape
        knn = hnswlib.Index(space=metric, dim=dim)
        knn.init_index(max_elements=ns, ef_construction=ef_c, M=M, random_seed=random_state)
        knn.add_items(X)
        knn.set_ef(ef)
        knn_indices, knn_distances = knn.knn_query(X, k=self.n_neighbors, num_threads=self.num_threads)
        n_neighbors = self.n_neighbors
        if metric == 'l2':
            knn_distances = np.sqrt(knn_distances)
        self.distances, self.connectivities = compute_connectivities_umap(knn_indices, knn_distances, ns, n_neighbors)
        self.knn_indices = knn_indices