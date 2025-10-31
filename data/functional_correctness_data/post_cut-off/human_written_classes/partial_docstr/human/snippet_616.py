class UnavailableNullContext:
    """A placeholder class for unavailable context managers

    This context manager will return a value which will throw an
    UnavailableError if used in any way, but the context manager itself can be
    safely invoked.
    """

    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        return UnavailableMeta('MissingContextValue', (), {'_msg': 'Attempted to make use of placeholder context return value.'})

    def __exit__(self, *args, **kwargs):
        pass