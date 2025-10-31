class _ImportCache:
    __slots__ = ['_ua', '_uq']

    def __init__(self):
        self._ua = None
        self._uq = None

    @property
    def ua(self):
        if self._ua is None:
            from unyt.array import unyt_array
            self._ua = unyt_array
        return self._ua

    @property
    def uq(self):
        if self._uq is None:
            from unyt.array import unyt_quantity
            self._uq = unyt_quantity
        return self._uq