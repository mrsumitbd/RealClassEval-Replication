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

    def evaluate(self, verbose=True, decode=True, passes=None, num_threads=1, apply_experimental_transforms=False):
        '''Summary
        Args:
            verbose (bool, optional): Description
            decode (bool, optional): Description
        Returns:
            TYPE: Description
        '''
        obj = self.expr
        if hasattr(obj, "evaluate") and callable(getattr(obj, "evaluate")):
            try:
                import inspect
                sig = inspect.signature(obj.evaluate)
                kwargs = {
                    "verbose": verbose,
                    "decode": decode,
                    "passes": passes,
                    "num_threads": num_threads,
                    "apply_experimental_transforms": apply_experimental_transforms,
                }
                filtered_kwargs = {k: v for k,
                                   v in kwargs.items() if k in sig.parameters}
                return obj.evaluate(**filtered_kwargs)
            except Exception:
                # Best-effort fallback with common kwargs
                try:
                    return obj.evaluate(verbose=verbose, decode=decode)
                except Exception:
                    return obj.evaluate()
        return obj
