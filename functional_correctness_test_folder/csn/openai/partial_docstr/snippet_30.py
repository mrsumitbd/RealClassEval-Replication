
import numpy as np
import weld


class LazyOpResult:
    '''Wrapper class around as yet un-evaluated Weld computation results
    Attributes:
        dim (int): Dimensionality of the output
        expr (WeldObject / Numpy.ndarray): The expression that needs to be
            evaluated
        weld_type (WeldType): Type of the output object
    '''

    def __init__(self, expr, weld_type, dim):
        self.expr = expr
        self.weld_type = weld_type
        self.dim = dim

    def evaluate(self, verbose=True, decode=True, passes=None,
                 num_threads=1, apply_experimental_transforms=False):
        """Evaluate the wrapped Weld expression.

        Parameters
        ----------
        verbose : bool, optional
            If True, prints a short description of the evaluation.
        decode : bool, optional
            If True, the result is decoded to a NumPy array.
        passes : list or None, optional
            Optional list of compiler passes to apply.
        num_threads : int, optional
            Number of threads to use during evaluation.
        apply_experimental_transforms : bool, optional
            Whether to enable experimental transforms.

        Returns
        -------
        WeldObject or np.ndarray
            The evaluated result, decoded to a NumPy array if ``decode`` is
            True.
        """
        if verbose:
            print(
                f"Evaluating LazyOpResult: dim={self.dim}, type={self.weld_type}")

        # If the expression is already a NumPy array, just return it
        if isinstance(self.expr, np.ndarray):
            result = self.expr
        else:
            # Evaluate the Weld expression
            result = weld.evaluate(
                self.expr,
                passes=passes,
                num_threads=num_threads,
                apply_experimental_transforms=apply_experimental_transforms,
            )

        # Decode to NumPy if requested
        if decode:
            result = weld.decode(result)

        return result
