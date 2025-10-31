import ctypes
import collections

class _GLFWgammaramp(ctypes.Structure):
    """
    Wrapper for:
        typedef struct GLFWgammaramp GLFWgammaramp;
    """
    _fields_ = [('red', ctypes.POINTER(ctypes.c_ushort)), ('green', ctypes.POINTER(ctypes.c_ushort)), ('blue', ctypes.POINTER(ctypes.c_ushort)), ('size', ctypes.c_uint)]
    GLFWgammaramp = collections.namedtuple('GLFWgammaramp', ['red', 'green', 'blue'])

    def __init__(self):
        ctypes.Structure.__init__(self)
        self.red = None
        self.red_array = None
        self.green = None
        self.green_array = None
        self.blue = None
        self.blue_array = None
        self.size = 0

    def wrap(self, gammaramp):
        """
        Wraps a nested python sequence.
        """
        red, green, blue = gammaramp
        size = min(len(red), len(green), len(blue))
        array_type = ctypes.c_ushort * size
        self.size = ctypes.c_uint(size)
        self.red_array = array_type()
        self.green_array = array_type()
        self.blue_array = array_type()
        if NORMALIZE_GAMMA_RAMPS:
            red = [value * 65535 for value in red]
            green = [value * 65535 for value in green]
            blue = [value * 65535 for value in blue]
        for i in range(self.size):
            self.red_array[i] = int(red[i])
            self.green_array[i] = int(green[i])
            self.blue_array[i] = int(blue[i])
        pointer_type = ctypes.POINTER(ctypes.c_ushort)
        self.red = ctypes.cast(self.red_array, pointer_type)
        self.green = ctypes.cast(self.green_array, pointer_type)
        self.blue = ctypes.cast(self.blue_array, pointer_type)

    def unwrap(self):
        """
        Returns a GLFWgammaramp object.
        """
        red = [self.red[i] for i in range(self.size)]
        green = [self.green[i] for i in range(self.size)]
        blue = [self.blue[i] for i in range(self.size)]
        if NORMALIZE_GAMMA_RAMPS:
            red = [value / 65535.0 for value in red]
            green = [value / 65535.0 for value in green]
            blue = [value / 65535.0 for value in blue]
        return self.GLFWgammaramp(red, green, blue)