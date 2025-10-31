import os
import io
import sys

class ProgressFileIO(io.FileIO):

    def __init__(self, path, *args, **kwargs):
        self._total_size = os.path.getsize(path)
        io.FileIO.__init__(self, path, *args, **kwargs)

    def read(self, size):
        count = self.tell() / size
        self.progress_bar(count, size, self._total_size)
        return io.FileIO.read(self, size)

    @staticmethod
    def progress_bar(count, block_size, total_size):
        block = 100 * block_size / float(total_size)
        progress = count * block
        if progress % 5 < 1.01 * block:
            msg = '\r[{:51}] ({:d}%)'.format(int(progress // 2) * '=' + '>', int(progress))
            sys.stdout.write(msg)
            sys.stdout.flush()