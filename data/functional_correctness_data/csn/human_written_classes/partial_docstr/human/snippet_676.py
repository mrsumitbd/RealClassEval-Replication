import ctypes
import collections

class _GLFWimage(ctypes.Structure):
    """
    Wrapper for:
        typedef struct GLFWimage GLFWimage;
    """
    _fields_ = [('width', ctypes.c_int), ('height', ctypes.c_int), ('pixels', ctypes.POINTER(ctypes.c_ubyte))]
    GLFWimage = collections.namedtuple('GLFWimage', ['width', 'height', 'pixels'])

    def __init__(self):
        ctypes.Structure.__init__(self)
        self.width = 0
        self.height = 0
        self.pixels = None
        self.pixels_array = None

    def wrap(self, image):
        """
        Wraps a nested python sequence or PIL/pillow Image.
        """
        if hasattr(image, 'size') and hasattr(image, 'convert'):
            self.width, self.height = image.size
            array_type = ctypes.c_ubyte * 4 * (self.width * self.height)
            self.pixels_array = array_type()
            pixels = image.convert('RGBA').getdata()
            for i, pixel in enumerate(pixels):
                self.pixels_array[i] = pixel
        else:
            self.width, self.height, pixels = image
            array_type = ctypes.c_ubyte * 4 * self.width * self.height
            self.pixels_array = array_type()
            for i in range(self.height):
                for j in range(self.width):
                    for k in range(4):
                        self.pixels_array[i][j][k] = pixels[i][j][k]
        pointer_type = ctypes.POINTER(ctypes.c_ubyte)
        self.pixels = ctypes.cast(self.pixels_array, pointer_type)

    def unwrap(self):
        """
        Returns a GLFWimage object.
        """
        pixels = [[[int(c) for c in p] for p in l] for l in self.pixels_array]
        return self.GLFWimage(self.width, self.height, pixels)