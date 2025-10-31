from sklearn.utils import check_array

class ArrayIndexer:

    def __init__(self, X):
        X = check_array(X, accept_sparse=True, dtype=None, force_all_finite=False, ensure_2d=False, allow_nd=True, ensure_min_samples=0, ensure_min_features=0, estimator=None)
        self.X = X

    def __call__(self, indices):
        return self.X[indices]