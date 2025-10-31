
import tempfile


class ClosableNamedTemporaryFile:

    def __init__(self):
        self.file = tempfile.NamedTemporaryFile(delete=False)

    def write(self, buf):
        self.file.write(buf)

    def close(self):
        self.file.close()

    def __del__(self):
        import os
        try:
            os.unlink(self.file.name)
        except AttributeError:
            pass
        except FileNotFoundError:
            pass
