class ExceptionCursorWrapper:
    """
    Wraps a cursor and raises an exception on any operation.
    Used in Templates panel.
    """

    def __init__(self, cursor, db, logger):
        pass

    def __getattr__(self, attr):
        raise SQLQueryTriggered()