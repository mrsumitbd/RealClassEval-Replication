class LazyOpResult:
    def __init__(self, expr, weld_type=None, dim=None):
        self.expr = expr
        self.weld_type = weld_type
        if dim is None or isinstance(dim, int):
            self.dim = dim
        elif isinstance(dim, (list, tuple)):
            self.dim = tuple(dim)
        else:
            raise TypeError("dim must be None, int, list, or tuple")

    def evaluate(self, verbose=True, decode=True, passes=None, num_threads=1, apply_experimental_transforms=False):
        def _call_callable(fn):
            try:
                return fn()
            except TypeError:
                try:
                    return fn(self)
                except TypeError:
                    return fn

        def _eval(expr):
            if hasattr(expr, "evaluate") and callable(getattr(expr, "evaluate")):
                try:
                    return expr.evaluate(
                        verbose=verbose,
                        decode=decode,
                        passes=passes,
                        num_threads=num_threads,
                        apply_experimental_transforms=apply_experimental_transforms,
                    )
                except TypeError:
                    return expr.evaluate()
            if callable(expr):
                return _call_callable(expr)
            if isinstance(expr, tuple) and expr and callable(expr[0]):
                fn = expr[0]
                args = expr[1] if len(expr) > 1 else ()
                kwargs = expr[2] if len(expr) > 2 and isinstance(
                    expr[2], dict) else {}
                try:
                    return fn(*args, **kwargs)
                except TypeError:
                    return fn()
            return expr

        result = _eval(self.expr)

        if decode:
            if isinstance(result, (bytes, bytearray, memoryview)):
                try:
                    result = bytes(result).decode("utf-8")
                except Exception:
                    result = bytes(result)

        return result
