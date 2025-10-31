
import abc


class Completer:

    @abc.abstractmethod
    def complete(self, original, pos):
        pass

    def relevant_part(self, original, pos):
        if pos < 0 or pos > len(original):
            return ""
        start = pos
        while start > 0 and original[start - 1] != ' ':
            start -= 1
        end = pos
        while end < len(original) and original[end] != ' ':
            end += 1
        return original[start:end]
