
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
        self._evaluated = False
        self._result = None

    def evaluate(self, verbose=True, decode=True, passes=None, num_threads=1, apply_experimental_transforms=False):
        '''Summary
        Args:
            verbose (bool, optional): Description
            decode (bool, optional): Description
        Returns:
            TYPE: Description
        '''
        if self._evaluated:
            return self._result

        # If expr is a numpy array, just return it
        try:
            import numpy as np
        except ImportError:
            np = None

        if np is not None and isinstance(self.expr, np.ndarray):
            self._result = self.expr
            self._evaluated = True
            return self._result

        # Otherwise, assume expr is a WeldObject and evaluate it
        # WeldObject is assumed to have an evaluate() method
        if hasattr(self.expr, 'evaluate'):
            result = self.expr.evaluate(
                verbose=verbose,
                decode=decode,
                passes=passes,
                num_threads=num_threads,
                apply_experimental_transforms=apply_experimental_transforms
            )
            self._result = result
            self._evaluated = True
            return self._result

        # Fallback: just return expr as is
        self._result = self.expr
        self._evaluated = True
        return self._result
