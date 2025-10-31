class _suppress_cleanup_errors:

    def __init__(self, context):
        self._context = context

    def __enter__(self):
        return self._context.__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            return self._context.__exit__(exc_type, exc_value, traceback)
        except PermissionError:
            pass