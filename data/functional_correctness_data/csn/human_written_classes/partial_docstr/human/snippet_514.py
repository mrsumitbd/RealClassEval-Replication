class _ParametersRestorer:
    """Context-manager to handle the reset of parameter values after an update."""

    def __init__(self, *, parameters, restore, refs=None):
        self._parameters = parameters
        self._restore = restore
        self._refs = {} if refs is None else refs

    def __enter__(self):
        return self._restore

    def __exit__(self, exc_type, exc_value, exc_tb):
        try:
            self._parameters._update(dict(self._restore, **self._refs))
        finally:
            self._restore = {}