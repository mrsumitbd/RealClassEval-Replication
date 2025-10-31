import numpy as np

class NumpyMemmapStorage:
    """
    Wraps a numpy memmap as a datastore for decoder state vectors.

    :param file_name: disk file path to store the memory-mapped file
    :param num_dim: number of dimensions of the vectors in the data store
    :param dtype: data type of the vectors in the data store
    """

    def __init__(self, file_name: str, num_dim: int, dtype: np.dtype) -> None:
        self.file_name = file_name
        self.num_dim = num_dim
        self.dtype = dtype
        self.block_size = -1
        self.mmap = None
        self.tail_idx = 0
        self.size = 0

    def open(self, initial_size: int, block_size: int) -> None:
        """Create a memmap handle and initialize its sizes."""
        self.mmap = np.memmap(self.file_name, dtype=self.dtype, mode='w+', shape=(initial_size, self.num_dim))
        self.size = initial_size
        self.block_size = block_size

    def add(self, array: np.ndarray) -> None:
        """
        It turns out that numpy memmap actually cannot be re-sized.
        So we have to pre-estimate how many entries we need and put it down as initial_size.
        If we end up adding more entries to the memmap than initially claimed, we'll have to bail out.

        :param array: the array of states to be added.
        """
        assert self.mmap is not None
        num_entries, num_dim = array.shape
        assert num_dim == self.num_dim
        if self.tail_idx + num_entries > self.size:
            logger.warning(f'Trying to write {num_entries} entries into a numpy memmap that ' + f'has size {self.size} and already has {self.tail_idx} entries. Nothing is written.')
        else:
            start = self.tail_idx
            end = self.tail_idx + num_entries
            self.mmap[start:end] = array
            self.tail_idx += num_entries