
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
