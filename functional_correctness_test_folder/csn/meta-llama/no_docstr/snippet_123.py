
import multiprocessing
from io import StringIO


class MultiprocessingStringIO:
    def __init__(self):
        self.manager = multiprocessing.Manager()
        self.queue = self.manager.Queue()
        self.buffer = StringIO()

    def getvalue(self):
        while not self.queue.empty():
            self.buffer.write(self.queue.get())
        return self.buffer.getvalue()

    def write(self, content):
        self.queue.put(content)

    def writelines(self, content_list):
        for content in content_list:
            self.write(content)
