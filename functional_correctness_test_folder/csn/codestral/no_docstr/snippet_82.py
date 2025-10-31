
import abc


class Completer(abc.ABC):

    @abc.abstractmethod
    def complete(self, original, pos):
        pass

    def relevant_part(self, original, pos):
        pass
