class KNNIndex:
    VALID_METRICS = []

    def __init__(self, data, k, metric='euclidean', metric_params=None, n_jobs=1, random_state=None, verbose=False):
        self.data = data
        self.n_samples = data.shape[0]
        self.k = k
        self.metric = self.check_metric(metric)
        self.metric_params = metric_params
        self.n_jobs = n_jobs
        self.random_state = random_state
        self.verbose = verbose
        self.index = None

    def build(self):
        """Build the nearest neighbor index on the training data.

        Builds an index on the training data and computes the nearest neighbors
        on the training data.

        Returns
        -------
        indices: np.ndarray
        distances: np.ndarray

        """

    def query(self, query, k):
        """Query the index with new points.

        Finds k nearest neighbors from the training data to each row of the
        query data.

        Parameters
        ----------
        query: array_like
        k: int

        Returns
        -------
        indices: np.ndarray
        distances: np.ndarray

        """

    def check_metric(self, metric):
        """Check that the metric is supported by the KNNIndex instance."""
        if callable(metric):
            pass
        elif metric not in self.VALID_METRICS:
            raise ValueError(f"`{self.__class__.__name__}` does not support the `{metric}` metric. Please choose one of the supported metrics: {', '.join(self.VALID_METRICS)}.")
        return metric