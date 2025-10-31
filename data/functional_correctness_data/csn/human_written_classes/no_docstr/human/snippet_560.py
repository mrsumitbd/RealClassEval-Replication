from ctypes import wintypes
import ctypes

class LUID(ctypes.Structure):
    _fields_ = [('low_part', wintypes.DWORD), ('high_part', wintypes.LONG)]

    def __eq__(self, other):
        return self.high_part == other.high_part and self.low_part == other.low_part

    def __ne__(self, other):
        return not self == other