class _PauliCtor:

    def __init__(self, ty):
        self.ty = ty

    def __call__(self, n):
        return self.ty(n)

    def __getitem__(self, n):
        return self.ty(n)

    @property
    def matrix(self):
        """Matrix reprentation of this operator."""
        return _matrix[self.ty.__name__[-1]].copy()