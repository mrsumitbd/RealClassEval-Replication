
import ctypes

# Define the native CK_MECHANISM structure


class CK_MECHANISM(ctypes.Structure):
    _fields_ = [
        ("mechanism", ctypes.c_ulong),      # CK_MECHANISM_TYPE
        ("pParameter", ctypes.c_void_p),    # void *
        ("ulParameterLen", ctypes.c_ulong)  # CK_ULONG
    ]


class Mechanism:
    '''Wraps CK_MECHANISM'''

    def __init__(self, mechanism, param=None):
        """
        Parameters
        ----------
        mechanism : int
            The CK_MECHANISM_TYPE value.
        param : bytes or None, optional
            Optional parameter data for the mechanism.
        """
        self.mechanism = mechanism
        self.param = param
        self._param_buffer = None  # keep a reference to avoid GC

    def to_native(self):
        """Convert mechanism to native CK_MECHANISM format."""
        if self.param is None:
            p_param = None
            ul_len = 0
        else:
            if not isinstance(self.param, (bytes, bytearray)):
                raise TypeError("param must be bytes or None")
            # Create a ctypes buffer that will stay alive
            self._param_buffer = ctypes.create_string_buffer(self.param)
            p_param = ctypes.cast(self._param_buffer, ctypes.c_void_p)
            ul_len = len(self.param)

        return CK_MECHANISM(
            mechanism=self.mechanism,
            pParameter=p_param,
            ulParameterLen=ul_len
        )
