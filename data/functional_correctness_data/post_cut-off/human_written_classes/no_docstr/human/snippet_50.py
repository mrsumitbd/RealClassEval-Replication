from typing import Callable, Any, List
import numpy as np
from dataclasses import dataclass

@dataclass
class SliceManipulator:
    size_func: Callable[[Any], int]
    slice_func: Callable[[Any, int, int], Any]
    concat_func: Callable[[List[Any]], Any]

    @classmethod
    def create_numpy_manipulator(cls, axis: int):

        def slice_numpy(x, start, end, slice_axis):
            indices = [slice(None)] * len(x.shape)
            indices[slice_axis] = slice(start, end)
            return x[tuple(indices)]
        manipulator = SliceManipulator(size_func=lambda x: x.shape[axis], slice_func=lambda x, start, end: slice_numpy(x, start, end, axis), concat_func=lambda x: np.concatenate(x, axis=axis))
        return manipulator