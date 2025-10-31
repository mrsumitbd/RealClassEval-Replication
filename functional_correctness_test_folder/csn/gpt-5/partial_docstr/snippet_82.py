import abc


class Completer(abc.ABC):

    @abc.abstractmethod
    def complete(self, original, pos):
        raise NotImplementedError

    def relevant_part(self, original, pos):
        '''
        Calculate the subword in a ' '-separated list of substrings of
        `original` that `pos` is in.
        '''
        if original is None:
            return ''
        if pos is None:
            pos = 0
        # Clamp pos to valid range
        pos = max(0, min(len(original), pos))

        # Start is one char after the last space before pos (or 0 if none)
        last_space = original.rfind(' ', 0, pos)
        start = last_space + 1

        # End is the next space at/after pos (or end of string if none)
        next_space = original.find(' ', pos)
        end = len(original) if next_space == -1 else next_space

        return original[start:end]
