import abc
import string


class Completer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def complete(self, original, pos):
        raise NotImplementedError

    def relevant_part(self, original, pos):
        if original is None:
            original = ""
        if pos is None:
            pos = len(original)
        pos = max(0, min(pos, len(original)))

        allowed = set(string.ascii_letters + string.digits + "_.")
        i = pos
        while i > 0 and original[i - 1] in allowed:
            i -= 1
        return original[i:pos]
