
from multiprocessing import Manager
from io import StringIO


class MultiprocessingStringIO:
    def __init__(self):
        self.manager = Manager()
        self.string_io = self.manager.list()

    def getvalue(self):
        return ''.join(self.string_io)

    def writelines(self, content_list):
        '''
        Shadow the StringIO.writelines method. Ingests a list and
        translates that to a string
        '''
        for content in content_list:
            self.string_io.append(content)

    def write(self, content):
        self.string_io.append(content)
