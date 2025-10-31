
from weld.weldobject import WeldObject
import numpy as np
from weld.types import WeldType


class LazyOpResult:
    '''Wrapper class around as yet un-evaluated Weld computation results
    Attributes:
        dim (int): Dimensionality of the output
        expr (WeldObject / Numpy.ndarray): The expression that needs to be
            evaluated
        weld_type (WeldType): Type of the output object
    '''

    def __init__(self, expr, weld_type, dim):
        '''Summary
        Args:
            expr (TYPE): Description
            weld_type (TYPE): Description
            dim (TYPE): Description
        '''
        self.expr = expr
        self.weld_type = weld_type
        self.dim = dim

    def evaluate(self, verbose=True, decode=True, passes=None, num_threads=1, apply_experimental_transforms=False):
        '''Summary
        Args:
            verbose (bool, optional): Description
            decode (bool, optional): Description
        Returns:
            TYPE: Description
        '''
        if isinstance(self.expr, WeldObject):
            result = self.expr.evaluate(
                verbose=verbose,
                passes=passes,
                num_threads=num_threads,
                apply_experimental_transforms=apply_experimental_transforms
            )
            if decode:
                if self.dim == 1:
                    return np.frombuffer(result, dtype=self.weld_type.numpy_dtype()).copy()
                elif self.dim > 1:
                    # Assuming the result is stored in row-major order
                    shape = result.size // np.dtype(
                        self.weld_type.numpy_dtype()).itemsize
                    shape = (shape,) if self.dim == 1 else (
                        shape // self.weld_type.numpy_dtype().itemsize, self.weld_type.numpy_dtype().itemsize)
                    return np.frombuffer(result, dtype=self.weld_type.numpy_dtype()).reshape(shape).copy()
                else:
                    return np.asscalar(np.frombuffer(result, dtype=self.weld_type.numpy_dtype()))
            else:
                return result
        elif isinstance(self.expr, np.ndarray):
            return self.expr
        else:
            raise ValueError("Unsupported expression type")
