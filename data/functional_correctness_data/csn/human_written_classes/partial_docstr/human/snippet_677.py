import ctypes
import collections

class _GLFWvidmode(ctypes.Structure):
    """
    Wrapper for:
        typedef struct GLFWvidmode GLFWvidmode;
    """
    _fields_ = [('width', ctypes.c_int), ('height', ctypes.c_int), ('red_bits', ctypes.c_int), ('green_bits', ctypes.c_int), ('blue_bits', ctypes.c_int), ('refresh_rate', ctypes.c_uint)]
    GLFWvidmode = collections.namedtuple('GLFWvidmode', ['size', 'bits', 'refresh_rate'])
    Size = collections.namedtuple('Size', ['width', 'height'])
    Bits = collections.namedtuple('Bits', ['red', 'green', 'blue'])

    def __init__(self):
        ctypes.Structure.__init__(self)
        self.width = 0
        self.height = 0
        self.red_bits = 0
        self.green_bits = 0
        self.blue_bits = 0
        self.refresh_rate = 0

    def wrap(self, video_mode):
        """
        Wraps a nested python sequence.
        """
        size, bits, self.refresh_rate = video_mode
        self.width, self.height = size
        self.red_bits, self.green_bits, self.blue_bits = bits

    def unwrap(self):
        """
        Returns a GLFWvidmode object.
        """
        size = self.Size(self.width, self.height)
        bits = self.Bits(self.red_bits, self.green_bits, self.blue_bits)
        return self.GLFWvidmode(size, bits, self.refresh_rate)