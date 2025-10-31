
class Enum:

    def __init__(self, *args, **kwargs):
        self._names = []
        self._map = {}
        # Handle positional arguments as names
        for idx, name in enumerate(args):
            self._names.append(name)
            self._map[idx] = name
        # Handle keyword arguments as name=value
        for name, val in kwargs.items():
            self._map[val] = name
            # Ensure names are in the correct order if possible
            if val == len(self._names):
                self._names.append(name)
            else:
                # Fill up to val with None if needed
                while len(self._names) <= val:
                    self._names.append(None)
                self._names[val] = name

    def __call__(self, val):
        '''Map an integer to the string representation.'''
        return self._map[val]
