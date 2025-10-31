import pycyphal.util
import pycyphal.transport

class OutgoingTransferIDCounter:
    """
    A member of the output transfer-ID map. Essentially this is just a boxed integer.
    The value is monotonically increasing starting from zero;
    transport-specific modulus is computed by the underlying transport(s).
    """

    def __init__(self) -> None:
        """
        Initializes the counter to zero.
        """
        self._value: int = 0

    def get_then_increment(self) -> int:
        """
        Samples the counter with post-increment; i.e., like ``i++``.
        """
        out = self._value
        self._value += 1
        return out

    def override(self, value: int) -> None:
        """
        Assigns a new value. Raises a :class:`ValueError` if the value is not a non-negative integer.
        """
        value = int(value)
        if value >= 0:
            self._value = value
        else:
            raise ValueError(f'Not a valid transfer-ID value: {value}')

    def __repr__(self) -> str:
        return pycyphal.util.repr_attributes(self, self._value)