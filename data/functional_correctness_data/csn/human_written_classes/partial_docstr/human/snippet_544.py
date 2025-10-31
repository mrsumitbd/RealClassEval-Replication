class FunctionSortKey:
    """Sort examples using a function passed through to :py:func:`sorted`.

    Parameters
    ----------
    func : :external+python:term:`callable`
           sorting key function,
           can only take one argument, i.e. lambda func = arg: arg[0] * arg[1]
    r : str, None
        printable representation of object
    """

    def __init__(self, func, r=None):
        self.f = func
        self.r = r

    def __repr__(self):
        return self.r if self.r else 'FunctionSortKey'

    def __call__(self, arg):
        """Return func(arg)."""
        return self.f(arg)