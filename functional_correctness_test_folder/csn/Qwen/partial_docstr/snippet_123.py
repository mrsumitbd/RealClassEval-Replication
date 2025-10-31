
import multiprocessing
from io import StringIO


class MultiprocessingStringIO:
    def __init__(self):
        self.manager = multiprocessing.Manager()
        self.shared_string = self.manager.Value('s', '')

    def getvalue(self):
        return self.shared_string.value

    def writelines(self, content_list):
        with self.shared_string.get_lock():
            self.shared_string.value += ''.join(content_list)
