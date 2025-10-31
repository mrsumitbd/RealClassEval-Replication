
from abc import ABC, abstractmethod
import os


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


class ConcreteFileLikeIO(FileLikeIO):

    def open(self, path, mode='r'):
        return open(path, mode)

    def exists(self, path):
        return os.path.exists(path)

    def remove(self, path):
        if self.exists(path):
            os.remove(path)
