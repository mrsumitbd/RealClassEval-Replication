
import io
import multiprocessing


class MultiprocessingStringIO:
    def __init__(self):
        self.buffer = multiprocessing.Manager().list()

    def getvalue(self):
        return ''.join(self.buffer)

    def writelines(self, content_list):
        for line in content_list:
            self.buffer.append(line)
