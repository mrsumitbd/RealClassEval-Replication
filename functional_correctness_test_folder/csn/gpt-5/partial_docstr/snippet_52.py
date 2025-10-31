class BitField:
    '''Convert an integer to a string for each bit.'''

    def __init__(self, *names):
        '''Initialize the list of named bits.'''
        # Allow either varargs of names or a single iterable of names
        if len(names) == 1 and isinstance(names[0], (list, tuple)):
            self.names = list(names[0])
        else:
            self.names = list(names)

    def __call__(self, val):
        try:
            val = int(val)
        except (TypeError, ValueError):
            raise ValueError("Value must be convertible to int")
        if val < 0:
            raise ValueError("Value must be non-negative")

        result = []
        i = 0
        v = val
        while v:
            if v & 1:
                if i < len(self.names):
                    result.append(str(self.names[i]))
                else:
                    result.append(str(i))
            v >>= 1
            i += 1

        return ', '.join(result)
