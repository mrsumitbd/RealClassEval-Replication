
import struct
from dataclasses import dataclass

# PKCS#11 mechanism identifier for AES CTR
CKM_AES_CTR = 0x0000010B  # typical value, adjust if needed


@dataclass
class AES_CTR_Mechanism:
    '''CKM_AES_CTR encryption mechanism'''
    counterBits: int
    counterBlock: bytes

    def __post_init__(self):
        if not isinstance(self.counterBits, int):
            raise TypeError("counterBits must be an integer")
        if not isinstance(self.counterBlock, (bytes, bytearray)):
            raise TypeError("counterBlock must be bytes")
        if len(self.counterBlock) != 16:
            raise ValueError("counterBlock must be 16 bytes long")

    def to_native(self):
        """
        Return a tuple suitable for use with a PKCS#11 library:
        (mechanism, parameter_bytes)
        where parameter_bytes is the packed CK_AES_CTR_PARAMS structure.
        """
        # Pack counterBits as unsigned long (little-endian)
        packed_bits = struct.pack("<I", self.counterBits)
        # Ensure counterBlock is bytes
        counter_block_bytes = bytes(self.counterBlock)
        # Combine into the parameter structure
        parameter = packed_bits + counter_block_bytes
        return (CKM_AES_CTR, parameter)
