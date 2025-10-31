import numpy as np
import pandas as pd

class Embedding:
    """
    Generates random embeddings of a given dimension 
    that aligns with the index of the dataframe

    """

    def __init__(self, df: pd.DataFrame):
        self.index = df.index

    def fit(self, n_dim: int):
        logger.info(f'-Creating Random Embedding of dimension {n_dim}')
        self.vectors = np.random.randn(len(self.index), n_dim)
        self.columns = [f'emb_{k}' for k in range(n_dim)]
        self.get_feature_names_out = callThrough(self.columns)

    def transform(self, ids) -> pd.DataFrame:
        mask = self.index.isin(ids)
        index = self.index[mask]
        res = self.vectors[mask]
        res = pd.DataFrame(res, index=index, columns=self.columns)
        return res

    def fit_transform(self, n_dim: int):
        self.fit(n_dim)
        return self.transform(self.index)