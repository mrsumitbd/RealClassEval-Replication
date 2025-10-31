
import abc


class Completer(abc.ABC):

    @abc.abstractmethod
    def complete(self, original, pos):
        pass

    def relevant_part(self, original, pos):
        parts = original.split(' ')
        cumulative_length = 0
        for part in parts:
            cumulative_length += len(part) + 1  # +1 for the space
            if pos < cumulative_length:
                return part
        return parts[-1] if parts else ''
