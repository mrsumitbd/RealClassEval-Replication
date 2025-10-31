class BitField:
    """Convert an integer to a string for each bit."""

    def __init__(self, *names):
        """Initialize the list of named bits."""
        self._names = names

    def __call__(self, val):
        """Return a list with a string for each True bit in the integer."""
        if not val:
            return None
        bits = []
        for n in self._names:
            if val & 1:
                bits.append(n)
            val >>= 1
            if not val:
                break
        return bits[0] if len(bits) == 1 else bits