class Enum:
    '''Map values to specific strings.'''

    def __init__(self, *args, **kwargs):
        '''Initialize the mapping.'''
        self._mapping = {}
        # Handle positional arguments: each is a string value
        for idx, val in enumerate(args):
            self._mapping[idx] = val
        # Handle keyword arguments: key may be an int (as string) or a name
        for key, val in kwargs.items():
            try:
                int_key = int(key)
                self._mapping[int_key] = val
            except (ValueError, TypeError):
                # Use next available index
                next_index = len(self._mapping)
                self._mapping[next_index] = val

    def __call__(self, val):
        '''Map an integer to the string representation.'''
        if val in self._mapping:
            return self._mapping[val]
        raise KeyError(f"Value {val!r} not found in Enum mapping.")
