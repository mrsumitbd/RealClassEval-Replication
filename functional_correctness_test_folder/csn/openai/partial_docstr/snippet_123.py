
import multiprocessing


class MultiprocessingStringIO:
    def __init__(self):
        # Use a Manager list to allow safe sharing between processes
        self._manager = multiprocessing.Manager()
        self._lines = self._manager.list()

    def getvalue(self):
        """Return the concatenated string of all written lines."""
        return ''.join(self._lines)

    def writelines(self, content_list):
        """
        Shadow the StringIO.writelines method.
        Accepts an iterable of strings and stores them in a shared list.
        """
        for line in content_list:
            self._lines.append(line)
