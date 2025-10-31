
import tempfile
import os


class ClosableNamedTemporaryFile:

    def __init__(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.file_path = self.temp_file.name

    def write(self, buf):
        self.temp_file.write(buf)

    def close(self):
        if not self.temp_file.closed:
            self.temp_file.close()

    def __del__(self):
        self.close()
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
