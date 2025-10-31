import os


class FileLikeIO:
    def open(self, path, mode='r'):
        return open(path, mode)

    def exists(self, path):
        return os.path.exists(path)

    def remove(self, path):
        os.remove(path)
