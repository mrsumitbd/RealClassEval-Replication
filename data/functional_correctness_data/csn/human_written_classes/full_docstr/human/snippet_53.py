class Bits:
    """Breaks an integer into a specified number of True/False bits."""

    def __init__(self, num_bits):
        """Initialize the number of bits."""
        self._bits = range(num_bits)

    def __call__(self, val):
        """Convert the integer to the list of True/False values."""
        return [bool(val >> i & 1) for i in self._bits]