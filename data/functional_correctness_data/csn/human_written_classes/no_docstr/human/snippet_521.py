class Kmeans:

    def __init__(self, K):
        self.K = K

    def fit(data):
        self.labels_ = k_means_clustering(data, self.K)

    def fit_transform(data):
        self.fit(data)
        return self.labels_