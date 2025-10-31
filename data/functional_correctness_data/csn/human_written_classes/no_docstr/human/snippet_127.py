class AgnosticBase:

    def __eq__(self, other):
        if isinstance(other, self.__class__) and hasattr(self, 'delegate') and hasattr(other, 'delegate'):
            return self.delegate == other.delegate
        return NotImplemented

    def __init__(self, delegate):
        self.delegate = delegate

    def __repr__(self):
        return f'{self.__class__.__name__}({self.delegate!r})'