import numpy as np
import array
import scipy.sparse as sparse
from typing import Dict, Generator, List, Optional, Tuple

class IncrementalSparseMatrixUInt16:

    def __init__(self, shape: Tuple[int, int]):
        self.dtype = np.uint16
        self.shape = shape
        self.rows = array.array('i')
        self.cols = array.array('i')
        self.data = array.array('H')

    def append(self, i: int, j: int, v: int) -> None:
        m, n = self.shape
        if i >= m or j >= n:
            raise Exception('Index out of bounds')
        self.rows.append(i)
        self.cols.append(j)
        self.data.append(v)

    def tocoo(self) -> sparse.coo_matrix:
        rows = np.frombuffer(self.rows, dtype=np.int32)
        cols = np.frombuffer(self.cols, dtype=np.int32)
        data = np.frombuffer(self.data, dtype=np.uint16)
        return sparse.coo_matrix((data, (rows, cols)), shape=self.shape)

    def __len__(self) -> int:
        return len(self.data)