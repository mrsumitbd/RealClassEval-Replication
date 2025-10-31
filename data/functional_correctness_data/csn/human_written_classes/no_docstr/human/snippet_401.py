import ctypes.wintypes
import ctypes

class BY_HANDLE_FILE_INFORMATION(ctypes.Structure):
    _fields_ = [('file_attributes', ctypes.wintypes.DWORD), ('creation_time', ctypes.wintypes.FILETIME), ('last_access_time', ctypes.wintypes.FILETIME), ('last_write_time', ctypes.wintypes.FILETIME), ('volume_serial_number', ctypes.wintypes.DWORD), ('file_size_high', ctypes.wintypes.DWORD), ('file_size_low', ctypes.wintypes.DWORD), ('number_of_links', ctypes.wintypes.DWORD), ('file_index_high', ctypes.wintypes.DWORD), ('file_index_low', ctypes.wintypes.DWORD)]

    @property
    def file_size(self):
        return (self.file_size_high << 32) + self.file_size_low

    @property
    def file_index(self):
        return (self.file_index_high << 32) + self.file_index_low