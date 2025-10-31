import ctypes
import ctypes.wintypes

class REPARSE_DATA_BUFFER(ctypes.Structure):
    _fields_ = [('tag', ctypes.c_ulong), ('data_length', ctypes.c_ushort), ('reserved', ctypes.c_ushort), ('substitute_name_offset', ctypes.c_ushort), ('substitute_name_length', ctypes.c_ushort), ('print_name_offset', ctypes.c_ushort), ('print_name_length', ctypes.c_ushort), ('flags', ctypes.c_ulong), ('path_buffer', ctypes.c_byte * 1)]

    def get_print_name(self):
        wchar_size = ctypes.sizeof(ctypes.wintypes.WCHAR)
        arr_typ = ctypes.wintypes.WCHAR * (self.print_name_length // wchar_size)
        data = ctypes.byref(self.path_buffer, self.print_name_offset)
        return ctypes.cast(data, ctypes.POINTER(arr_typ)).contents.value

    def get_substitute_name(self):
        wchar_size = ctypes.sizeof(ctypes.wintypes.WCHAR)
        arr_typ = ctypes.wintypes.WCHAR * (self.substitute_name_length // wchar_size)
        data = ctypes.byref(self.path_buffer, self.substitute_name_offset)
        return ctypes.cast(data, ctypes.POINTER(arr_typ)).contents.value