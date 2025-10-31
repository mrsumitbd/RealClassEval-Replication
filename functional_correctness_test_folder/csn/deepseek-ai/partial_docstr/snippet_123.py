
import io
from multiprocessing import Lock


class MultiprocessingStringIO:
    def __init__(self):
        self._stringio = io.StringIO()
        self._lock = Lock()

    def getvalue(self):
        with self._lock:
            return self._stringio.getvalue()

    def writelines(self, content_list):
        '''
        Shadow the StringIO.writelines method. Ingests a list and
        translates that to a string
        '''
        with self._lock:
            self._stringio.writelines(content_list)
