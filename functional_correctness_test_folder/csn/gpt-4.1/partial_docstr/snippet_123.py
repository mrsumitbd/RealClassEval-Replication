
import multiprocessing


class MultiprocessingStringIO:
    def __init__(self):
        self._manager = multiprocessing.Manager()
        self._list = self._manager.list()

    def getvalue(self):
        return ''.join(self._list)

    def writelines(self, content_list):
        # Accepts a list of strings and appends them to the internal list
        self._list.extend(str(item) for item in content_list)
