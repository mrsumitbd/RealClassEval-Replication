class Enum:
    '''Map values to specific strings.'''

    def __init__(self, *args, **kwargs):
        '''Initialize the mapping.'''
        self._map = {}

        def add_pair(k, v):
            self._map[int(k)] = str(v)

        if args:
            if len(args) == 1 and isinstance(args[0], dict):
                for k, v in args[0].items():
                    add_pair(k, v)
            elif len(args) == 1 and isinstance(args[0], (list, tuple)):
                seq = args[0]
                if all(isinstance(x, (list, tuple)) and len(x) == 2 for x in seq):
                    for k, v in seq:
                        add_pair(k, v)
                else:
                    for i, name in enumerate(seq):
                        add_pair(i, name)
            else:
                if all(isinstance(x, str) for x in args):
                    for i, name in enumerate(args):
                        add_pair(i, name)
                elif all(isinstance(x, (list, tuple)) and len(x) == 2 for x in args):
                    for k, v in args:
                        add_pair(k, v)
                else:
                    raise TypeError(
                        "Unsupported positional arguments for Enum.")
        for k, v in kwargs.items():
            add_pair(k, v)

    def __call__(self, val):
        '''Map an integer to the string representation.'''
        try:
            return self._map[int(val)]
        except Exception:
            return str(val)
