class OutStream:

    def __init__(self, f):
        self.f = f

    def __lshift__(self, x):
        """Emulate the much liked C++ syntax for chaining output."""
        if isinstance(x, list):
            self.f.write(make_escape(*x))
            self.f.flush()
            return self
        if isinstance(x, str):
            self.f.write(x)
            self.f.flush()
            return self
        raise TypeError