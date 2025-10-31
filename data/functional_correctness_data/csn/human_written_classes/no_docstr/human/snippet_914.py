class PrintState:

    def __init__(self, sep=None, add=None):
        self.sep = sep if sep is not None else '\n'
        self.add = add if add is not None else '    '

    def copy(self, sep=None, add=None):
        return PrintState(self.sep if sep is None else sep, self.add if add is None else add)