
from abc import ABC, abstractmethod


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
