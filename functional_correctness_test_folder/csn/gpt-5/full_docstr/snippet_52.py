class BitField:
    '''Convert an integer to a string for each bit.'''

    def __init__(self, *names):
        '''Initialize the list of named bits.'''
        self._names = list(names)

    def __call__(self, val):
        '''Return a list with a string for each True bit in the integer.'''
        if not isinstance(val, int):
            raise TypeError("BitField expects an integer value")
        result = []
        i = 0
        n = val
        while n:
            if n & 1:
                if i < len(self._names) and self._names[i] is not None:
                    result.append(self._names[i])
                else:
                    result.append(str(i))
            n >>= 1
            i += 1
        return result
