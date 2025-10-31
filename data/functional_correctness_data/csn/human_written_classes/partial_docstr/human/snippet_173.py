class coeff_func:
    """This is a decorator class used later to construct nice names"""

    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):

        def __repr__():
            s = self.f.__doc__.replace('alpha', '%.4f' % kwargs['alpha']).replace('beta', '%.4f' % kwargs['beta'])
            return s
        self.__doc__ = __repr__()
        self.__repr__ = __repr__
        self.__str__ = __repr__
        return self.f(*args, **kwargs)