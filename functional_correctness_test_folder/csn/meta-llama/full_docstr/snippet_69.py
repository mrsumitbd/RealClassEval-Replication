
from abc import ABC, abstractmethod


class BaseStorage(ABC):
    '''Base class of backend storage'''
    @abstractmethod
    def write(self, id, data):
        '''Abstract interface of writing data
        Args:
            id (str): unique id of the data in the storage.
            data (bytes or str): data to be stored.
        '''
        pass

    @abstractmethod
    def exists(self, id):
        '''Check the existence of some data
        Args:
            id (str): unique id of the data in the storage
        Returns:
            bool: whether the data exists
        '''
        pass

    @abstractmethod
    def max_file_idx(self):
        '''Get the max existing file index
        Returns:
            int: the max index
        '''
        pass


class LocalStorage(BaseStorage):
    def __init__(self, storage_dir):
        import os
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def write(self, id, data):
        if isinstance(data, str):
            data = data.encode()
        with open(f'{self.storage_dir}/{id}', 'wb') as f:
            f.write(data)

    def exists(self, id):
        import os
        return os.path.exists(f'{self.storage_dir}/{id}')

    def max_file_idx(self):
        import os
        files = [f for f in os.listdir(self.storage_dir) if os.path.isfile(
            os.path.join(self.storage_dir, f))]
        if not files:
            return -1
        return max(int(f) for f in files)


class InMemoryStorage(BaseStorage):
    def __init__(self):
        self.data = {}

    def write(self, id, data):
        if isinstance(data, str):
            data = data.encode()
        self.data[id] = data

    def exists(self, id):
        return id in self.data

    def max_file_idx(self):
        indices = [int(id) for id in self.data.keys() if id.isdigit()]
        if not indices:
            return -1
        return max(indices)


# Example usage
if __name__ == "__main__":
    storage = LocalStorage('./storage')
    storage.write('1', 'Hello, world!')
    print(storage.exists('1'))  # True
    print(storage.max_file_idx())  # 1

    in_memory_storage = InMemoryStorage()
    in_memory_storage.write('1', 'Hello, world!')
    print(in_memory_storage.exists('1'))  # True
    print(in_memory_storage.max_file_idx())  # 1
