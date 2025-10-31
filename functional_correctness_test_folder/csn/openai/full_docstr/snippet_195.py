
import struct
from typing import Union, Iterable


class KEY_DERIVATION_STRING_DATA_MechanismBase:
    """Base class for mechanisms using derivation string data."""

    def __init__(self, data: Union[bytes, bytearray, Iterable[int]], mechType: int):
        """
        :param data: a byte array to concatenate the key with
        :param mechType: mechanism type (integer)
        """
        if isinstance(data, (bytes, bytearray)):
            self.data = bytes(data)
        else:
            try:
                self.data = bytes(data)
            except Exception as exc:
                raise TypeError(
                    "data must be bytes-like or an iterable of ints") from exc

        if not isinstance(mechType, int):
            raise TypeError("mechType must be an integer")
        self.mechType = mechType

    def to_native(self) -> bytes:
        """
        Convert mechanism to a native binary format.

        The format is:
        - 4 bytes: mechType (big-endian unsigned int)
        - 4 bytes: length of data (big-endian unsigned int)
        - N bytes: data
        """
        header = struct.pack(">II", self.mechType, len(self.data))
        return header + self.data

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(mechType={self.mechType}, "
            f"data={self.data!r})"
        )
