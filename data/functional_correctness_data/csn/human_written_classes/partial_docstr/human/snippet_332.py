class option_context:
    """
    Context manager to temporarily set options in the `with` statement context.

    You need to invoke as ``option_context(pat, val, [(pat, val), ...])``.

    Examples
    --------

    >>> with option_context('display.max_rows', 10, 'display.max_columns', 5):
            ...

    """

    def __init__(self, *args):
        if not (len(args) % 2 == 0 and len(args) >= 2):
            raise ValueError('Need to invoke asoption_context(pat, val, [(pat, val), ...)).')
        self.ops = list(zip(args[::2], args[1::2]))

    def __enter__(self):
        undo = []
        for pat, _ in self.ops:
            undo.append((pat, _get_option(pat, silent=True)))
        self.undo = undo
        for pat, val in self.ops:
            _set_option(pat, val, silent=True)

    def __exit__(self, *args):
        if self.undo:
            for pat, val in self.undo:
                _set_option(pat, val, silent=True)