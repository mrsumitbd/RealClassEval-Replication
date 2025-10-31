class Array:
    def __init__(self, fmt):
        self.fmt = fmt

    def __call__(self, buf):
        import array
        return array.array(self.fmt, buf)
