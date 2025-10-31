from os import path
import numpy as np
import gzip
import pickle

class TSNEBenchmark:
    perplexity = 30
    learning_rate = 200
    n_jobs = 1

    def run(self, n_samples=1000, random_state=None):
        raise NotImplementedError()

    def run_multiple(self, n=5, n_samples=1000):
        for idx in range(n):
            self.run(n_samples=n_samples, random_state=idx)

    def load_data(self, n_samples=None):
        with gzip.open(path.join('data', '10x_mouse_zheng.pkl.gz'), 'rb') as f:
            data = pickle.load(f)
        x, y = (data['pca_50'], data['CellType1'])
        if n_samples is not None:
            indices = np.random.choice(list(range(x.shape[0])), n_samples, replace=False)
            x, y = (x[indices], y[indices])
        return (x, y)