
from abc import ABC, abstractmethod
import os


class BaseStorage(ABC):

    @abstractmethod
    def write(self, id, data):
        pass

    @abstractmethod
    def exists(self, id):
        pass

    @abstractmethod
    def max_file_idx(self):
        pass


class FileStorage(BaseStorage):
    def __init__(self, storage_dir):
        self.storage_dir = storage_dir
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

    def write(self, id, data):
        file_path = os.path.join(self.storage_dir, f'{id}.dat')
        with open(file_path, 'wb') as f:
            f.write(data)

    def exists(self, id):
        file_path = os.path.join(self.storage_dir, f'{id}.dat')
        return os.path.exists(file_path)

    def max_file_idx(self):
        files = [f for f in os.listdir(self.storage_dir) if f.endswith('.dat')]
        if not files:
            return -1
        idxs = [int(f.split('.')[0]) for f in files]
        return max(idxs)


# Example usage:
if __name__ == "__main__":
    storage = FileStorage('storage')
    storage.write(1, b'Hello, world!')
    print(storage.exists(1))  # True
    print(storage.exists(2))  # False
    storage.write(2, b'Another file')
    print(storage.max_file_idx())  # 2
