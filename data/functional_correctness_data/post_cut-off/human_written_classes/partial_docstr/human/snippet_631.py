class PyOnlyDef:
    """Exportable that does not export but can be resolved in Python."""
    __slots__ = ['py_value']

    def __init__(self, py_value):
        self.py_value = py_value

    def __str__(self):
        return str(self.py_value)

    def __repr__(self):
        return repr(self.py_value)

    def __call__(self, *args, **kwargs):
        return self.py_value(*args, **kwargs)