import math
from typing import Iterator, Optional, Tuple, Union
from deeppavlov.core.data.data_learning_iterator import DataLearningIterator

class SingleTaskBatchGenerator:
    """
    Batch generator for a single task.
    If there are no elements in the dataset to form another batch, Nones are returned.
    Args:
        dataset_iterator: dataset iterator from which batches are drawn.
        batch_size: size fo the batch.
        data_type: "train", "valid", or "test"
        shuffle: whether dataset will be shuffled.
        n_batches: the number of batches that will be generated.
    """

    def __init__(self, dataset_iterator: Union[DataLearningIterator], batch_size: int, data_type: str, shuffle: bool, n_batches: Optional[int]=None, size_of_last_batch: Optional[int]=None):
        self.dataset_iterator = dataset_iterator
        self.batch_size = batch_size
        self.data_type = data_type
        self.shuffle = shuffle
        self.n_batches = n_batches
        self.size_of_last_batch = self.batch_size if size_of_last_batch is None else size_of_last_batch
        self.inner_batch_size = math.gcd(len(self.dataset_iterator.data[data_type]), batch_size)
        self.gen = self.dataset_iterator.gen_batches(self.inner_batch_size, self.data_type, self.shuffle)
        self.batch_count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.n_batches is not None and self.batch_count > self.n_batches:
            raise StopIteration
        x, y = ((), ())
        while len(x) < self.batch_size or len(y) < self.batch_size:
            try:
                xx, yy = next(self.gen)
                x += xx
                y += yy
            except StopIteration:
                x_nones = tuple([None for _ in range(self.batch_size)])
                y_nones = x_nones
                return (x_nones, y_nones)
        self.batch_count += 1
        if self.batch_count == self.n_batches:
            x = x[:self.size_of_last_batch]
            y = y[:self.size_of_last_batch]
        return (x, y)