class _Undefined:
    """
    Dummy value to signal completely undefined values rather than
    simple None values.
    """

    def __bool__(self):
        raise RuntimeError('Use `is` to compare Undefined')

    def __repr__(self):
        return '<Undefined>'