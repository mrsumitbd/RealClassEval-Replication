
import abc


class Completer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def complete(self, original, pos):
        pass

    def relevant_part(self, original, pos):
        return original[:pos]
