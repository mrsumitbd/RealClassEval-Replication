
import struct
from typing import Any


class EXTRACT_KEY_FROM_KEY_Mechanism:
    """
    Mechanism for extracting a sub‑key from an existing key.

    Parameters
    ----------
    extractParams : int
        The index (in bits) of the first bit of the original key that
        should be used in the newly derived key.  Bits before this
        index are discarded.  For example, if ``extractParams`` is
        ``5`` then the first five bits of the original key are
        ignored.
    """

    def __init__(self, extractParams: int):
        if not isinstance(extractParams, int):
            raise TypeError(
                f"extractParams must be an int, got {type(extractParams).__name__}"
            )
        if extractParams < 0:
            raise ValueError("extractParams must be non‑negative")
        self.extractParams = extractParams

    def to_native(self) -> bytes:
        """
        Return a native representation of the mechanism parameters.

        The PKCS#11 specification defines the parameter for
        CKM_EXTRACT_KEY_FROM_KEY as a 32‑bit unsigned integer
        representing the bit index.  This method returns the
        little‑endian packed representation of that integer.
        """
        return struct.pack("<I", self.extractParams)

    # Optional helper for clarity (not required by the skeleton)
    def extract(self, key: bytes) -> bytes:
        """
        Extract a sub‑key from ``key`` starting at the bit index
        specified by ``extractParams``.

        Parameters
        ----------
        key : bytes
            The original key from which to extract a sub‑key.

        Returns
        -------
        bytes
            The extracted sub‑key.
        """
        bit_index = self.extractParams
        byte_index = bit_index // 8
        bit_offset = bit_index % 8

        if byte_index >= len(key):
            return b""

        # If there is a bit offset, we need to shift the bytes
        if bit_offset == 0:
            return key[byte_index:]

        # Shift left to discard the leading bits
        shifted = bytearray()
        carry = 0
        for b in key[byte_index:]:
            new_carry = b >> (8 - bit_offset)
            shifted.append((b << bit_offset) & 0xFF | carry)
            carry = new_carry
        if carry:
            shifted.append(carry)

        return bytes(shifted)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(extractParams={self.extractParams})"
