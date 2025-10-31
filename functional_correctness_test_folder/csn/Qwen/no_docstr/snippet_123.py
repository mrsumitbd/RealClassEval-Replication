
import multiprocessing
from io import StringIO


class MultiprocessingStringIO:
    def __init__(self):
        self.manager = multiprocessing.Manager()
        self.shared_string = self.manager.list()

    def getvalue(self):
        return ''.join(self.shared_string)

    def writelines(self, content_list):
        for content in content_list:
            self.shared_string.append(content)
