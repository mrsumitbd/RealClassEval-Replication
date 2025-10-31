import shutil
import tempfile

class TemporaryDirectory:

    def __enter__(self):
        self.tempdir = tempfile.mkdtemp()
        return self.tempdir

    def __exit__(self, type_, value, traceback):
        shutil.rmtree(self.tempdir)