import ctypes
import collections

class _GLFWgamepadstate(ctypes.Structure):
    """
    Wrapper for:
        typedef struct GLFWgamepadstate GLFWgamepadstate;
    """
    _fields_ = [('buttons', ctypes.c_ubyte * 15), ('axes', ctypes.c_float * 6)]
    GLFWgamepadstate = collections.namedtuple('GLFWgamepadstate', ['buttons', 'axes'])

    def __init__(self):
        ctypes.Structure.__init__(self)
        self.buttons = (ctypes.c_ubyte * 15)(*[0] * 15)
        self.axes = (ctypes.c_float * 6)(*[0] * 6)

    def wrap(self, gamepad_state):
        """
        Wraps a nested python sequence.
        """
        buttons, axes = gamepad_state
        for i in range(15):
            self.buttons[i] = buttons[i]
        for i in range(6):
            self.axes[i] = axes[i]

    def unwrap(self):
        """
        Returns a GLFWvidmode object.
        """
        buttons = [int(button) for button in self.buttons]
        axes = [float(axis) for axis in self.axes]
        return self.GLFWgamepadstate(buttons, axes)