class _SortKey:
    """Base class for section order key classes."""

    def __init__(self, src_dir):
        self.src_dir = src_dir

    def __repr__(self):
        return f'<{self.__class__.__name__}>'