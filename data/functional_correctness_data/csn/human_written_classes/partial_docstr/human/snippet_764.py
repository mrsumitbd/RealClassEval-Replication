class Dispatch:
    """
    The Dispatch class, care of David Ascher, allows different functions to
    be called depending on the argument types.  This way, there can be one
    function name regardless of the argument type.  To access function doc
    in stats.py module, prefix the function with an 'l' or 'a' for list or
    array arguments, respectively.  That is, print stats.lmean.__doc__ or
    print stats.amean.__doc__ or whatever."""

    def __init__(self, *tuples):
        self._dispatch = {}
        for func, types in tuples:
            for t in types:
                if t in self._dispatch.keys():
                    raise ValueError("can't have two dispatches on " + str(t))
                self._dispatch[t] = func
        self._types = list(self._dispatch.keys())

    def __call__(self, arg1, *args, **kw):
        if type(arg1) not in self._types:
            raise TypeError(f"don't know how to dispatch {type(arg1)} arguments")
        return self._dispatch[type(arg1)](*(arg1,) + args, **kw)