class LazyOpResult:
    '''Wrapper class around as yet un-evaluated Weld computation results
    Attributes:
        dim (int): Dimensionality of the output
        expr: The expression that needs to be evaluated (e.g., WeldObject, numpy array, etc.)
        weld_type: Type of the output object (optional, used by some runtimes)
    '''

    def __init__(self, expr, weld_type=None, dim=None):
        '''Initialize a LazyOpResult.
        Args:
            expr: The expression or concrete value.
            weld_type: Optional type info for backends.
            dim: Optional dimensionality information.
        '''
        self.expr = expr
        self.weld_type = weld_type
        self.dim = dim

    def _try_evaluate(self, obj, kwargs):
        # Attempt calling obj.evaluate with descending kwargs compatibility
        if not hasattr(obj, "evaluate"):
            return obj

        evaluate = getattr(obj, "evaluate")
        try:
            return evaluate(**kwargs)
        except TypeError:
            # Retry with subsets of kwargs for broader compatibility
            order = [
                ("verbose", "decode", "passes", "num_threads",
                 "apply_experimental_transforms"),
                ("verbose", "decode", "passes", "num_threads"),
                ("verbose", "decode", "passes"),
                ("verbose", "decode"),
                ("decode",),
                tuple(),  # no kwargs
            ]
            for keys in order:
                sub_kwargs = {k: kwargs[k] for k in keys if k in kwargs}
                try:
                    return evaluate(**sub_kwargs)
                except TypeError:
                    continue
            # Final attempt: call without kwargs
            return evaluate()

    def _maybe_decode(self, value, decode):
        if not decode:
            return value

        # If value is another LazyOpResult, evaluate it fully
        if isinstance(value, LazyOpResult):
            return value.evaluate(decode=decode)

        # Common decoding methods
        for attr in ("to_numpy", "to_ndarray", "to_list", "tolist", "numpy"):
            if hasattr(value, attr) and callable(getattr(value, attr)):
                try:
                    return getattr(value, attr)()
                except Exception:
                    pass

        # Numpy buffer protocol support (array interface)
        if hasattr(value, "__array__"):
            try:
                import numpy as np  # optional
                return np.array(value)
            except Exception:
                return value

        return value

    def evaluate(self, verbose=True, decode=True, passes=None, num_threads=1, apply_experimental_transforms=False):
        '''Evaluate the underlying expression and optionally decode the result.
        Args:
            verbose (bool, optional): Verbose evaluation (if supported by backend).
            decode (bool, optional): Attempt to convert backend result to a Python/native object.
            passes: Optional optimization passes for backend.
            num_threads (int, optional): Number of threads for evaluation (if supported).
            apply_experimental_transforms (bool, optional): Enable experimental transforms (if supported).
        Returns:
            The evaluated (and optionally decoded) result.
        '''
        # If already a concrete value
        if isinstance(self.expr, LazyOpResult):
            result = self.expr.evaluate(
                verbose=verbose,
                decode=decode,
                passes=passes,
                num_threads=num_threads,
                apply_experimental_transforms=apply_experimental_transforms,
            )
            return result

        # If expr is a callable, call it without assumptions
        if callable(self.expr) and not hasattr(self.expr, "evaluate"):
            try:
                result = self.expr()
            except TypeError:
                # If it needs context, give best-effort: pass known kwargs if accepted
                result = self.expr
        else:
            # Try backend-style evaluate
            kwargs = {
                "verbose": verbose,
                "decode": decode,
                "passes": passes,
                "num_threads": num_threads,
                "apply_experimental_transforms": apply_experimental_transforms,
            }
            result = self._try_evaluate(self.expr, kwargs)

        # Optionally decode the result into a native object
        return self._maybe_decode(result, decode)

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}(expr={type(self.expr).__name__}, weld_type={self.weld_type}, dim={self.dim})"
