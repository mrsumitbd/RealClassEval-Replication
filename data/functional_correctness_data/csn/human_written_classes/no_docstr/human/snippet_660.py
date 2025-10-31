from functools import wraps

class SympyWrapper:

    @classmethod
    def as_decorator(cls, func=None, **kwargs):
        self = cls(**kwargs)
        if func is not None and (not kwargs):
            return self(func)
        return self

    def __init__(self, func=None, var=None, include_G=True):
        var_ = 'x, y, z' if var is None else var
        self.var = var_
        self.include_G = include_G

    def __call__(self, wrapped_function):

        @wraps(wrapped_function)
        def wrapper(cls, *func_args, **func_kwargs):
            try:
                import sympy as sy
            except ImportError as e:
                raise ImportError('Converting to a latex expression requires the sympy package to be installed') from e
            var = sy.symbols(self.var, seq=True, real=True)
            var = {v.name: v for v in var}
            if cls._parameters:
                par = sy.symbols(' '.join(cls._parameters.keys()), seq=True, real=True)
                par = {v.name: v for v in par}
            else:
                par = {}
            if self.include_G:
                par['G'] = sy.symbols('G')
            return wrapped_function(cls, var, par)
        return wrapper