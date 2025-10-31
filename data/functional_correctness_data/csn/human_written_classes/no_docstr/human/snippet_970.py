class CancellationContext:

    def __init__(self):
        self._is_cancelled = False
        ':type : bool'

    @property
    def is_cancelled(self):
        return self._is_cancelled