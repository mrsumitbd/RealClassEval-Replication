
import numpy as np


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
            expr (WeldObject / Numpy.ndarray): The expression to evaluate
            weld_type (WeldType): The expected Weld type of the result
            dim (int): Dimensionality of the output
        '''
        self.expr = expr
        self.weld_type = weld_type
        self.dim = dim
        self._evaluated = None

    def evaluate(self, verbose=True, decode=True, passes=None,
                 num_threads=1, apply_experimental_transforms=False):
        '''Evaluate the wrapped expression.

        Args:
            verbose (bool, optional): If True, print progress information.
            decode (bool, optional): If True and the result is a WeldObject,
                attempt to decode it into a NumPy array.
            passes (list[str] | None, optional): List of optimization passes
                to apply during evaluation.
            num_threads (int, optional): Number of threads to use for
                evaluation.
            apply_experimental_transforms (bool, optional): Whether to apply
                experimental transforms.

        Returns:
            The evaluated result, typically a NumPy array.
        '''
        # Return cached result if already evaluated
        if self._evaluated is not None:
            return self._evaluated

        # If the expression is already a NumPy array, just return it
        if isinstance(self.expr, np.ndarray):
            self._evaluated = self.expr
            return self._evaluated

        # If the expression has an `evaluate` method, use it
        if hasattr(self.expr, 'evaluate'):
            eval_kwargs = {}
            if verbose is not None:
                eval_kwargs['verbose'] = verbose
            if decode is not None:
                eval_kwargs['decode'] = decode
            if passes is not None:
                eval_kwargs['passes'] = passes
            if num_threads is not None:
                eval_kwargs['num_threads'] = num_threads
            if apply_experimental_transforms is not None:
                eval_kwargs['apply_experimental_transforms'] = apply_experimental_transforms
            result = self.expr.evaluate(**eval_kwargs)
            self._evaluated = result
            return result

        # If the expression is a callable, call it
        if callable(self.expr):
            result = self.expr()
            self._evaluated = result
            return result

        # Unsupported expression type
        raise TypeError(
            f"Unsupported expression type for evaluation: {type(self.expr)}")
