
from abc import ABC, abstractmethod


class FileLikeIO(ABC):

    @abstractmethod
    def open(self, path, mode='r'):
        pass

    @abstractmethod
    def exists(self, path):
        pass

    @abstractmethod
    def remove(self, path):
        pass


class LocalFileIO(FileLikeIO):
    def open(self, path, mode='r'):
        return open(path, mode)

    def exists(self, path):
        import os
        return os.path.exists(path)

    def remove(self, path):
        import os
        os.remove(path)


class InMemoryFileIO(FileLikeIO):
    def __init__(self):
        self.files = {}

    def open(self, path, mode='r'):
        if mode == 'r':
            if path not in self.files:
                raise FileNotFoundError(f"File {path} not found")
            return self._open_for_read(path)
        elif mode == 'w':
            return self._open_for_write(path)
        else:
            raise ValueError("Unsupported mode")

    def _open_for_read(self, path):
        return InMemoryFileReader(self.files[path])

    def _open_for_write(self, path):
        return InMemoryFileWriter(self, path)

    def exists(self, path):
        return path in self.files

    def remove(self, path):
        if path in self.files:
            del self.files[path]
        else:
            raise FileNotFoundError(f"File {path} not found")


class InMemoryFileReader:
    def __init__(self, content):
        self.content = content
        self.position = 0

    def read(self, size=None):
        if size is None:
            data = self.content[self.position:]
            self.position = len(self.content)
        else:
            data = self.content[self.position:self.position + size]
            self.position += size
        return data

    def close(self):
        pass


class InMemoryFileWriter:
    def __init__(self, file_io, path):
        self.file_io = file_io
        self.path = path
        self.content = ''

    def write(self, data):
        self.content += data

    def close(self):
        self.file_io.files[self.path] = self.content


# Example usage
if __name__ == "__main__":
    local_io = LocalFileIO()
    with local_io.open('test.txt', 'w') as f:
        f.write('Hello, world!')
    print(local_io.exists('test.txt'))  # True
    local_io.remove('test.txt')
    print(local_io.exists('test.txt'))  # False

    in_memory_io = InMemoryFileIO()
    with in_memory_io.open('test.txt', 'w') as f:
        f.write('Hello, world!')
    print(in_memory_io.exists('test.txt'))  # True
    with in_memory_io.open('test.txt', 'r') as f:
        print(f.read())  # Hello, world!
    in_memory_io.remove('test.txt')
    print(in_memory_io.exists('test.txt'))  # False
