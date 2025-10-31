class CfgStruct:
    """
    A simple class containing a bunch of fields. Equivalent to Python3
    SimpleNamespace
    """

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __repr__(self):
        return '<' + ' '.join(('{}={!r}'.format(*kv) for kv in self.__dict__.items())) + '>'