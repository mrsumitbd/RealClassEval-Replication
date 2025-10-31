from multiprocessing import Manager


class MultiprocessingStringIO:
    '''
    Provide a StringIO-like interface to the multiprocessing ListProxy. The
    multiprocessing ListProxy needs to be instantiated before the flaky plugin
    is configured, so the list is created as a class variable.
    '''
    _manager = Manager()
    _buffer = _manager.list()

    def _to_str(self, obj):
        if isinstance(obj, bytes):
            try:
                return obj.decode()
            except Exception:
                return obj.decode(errors='replace')
        return str(obj)

    def getvalue(self):
        '''
        Shadow the StringIO.getvalue method.
        '''
        return ''.join(self._buffer)

    def writelines(self, content_list):
        '''
        Shadow the StringIO.writelines method. Ingests a list and
        translates that to a string
        '''
        for item in content_list:
            self._buffer.append(self._to_str(item))

    def write(self, content):
        '''
        Shadow the StringIO.write method.
        '''
        s = self._to_str(content)
        self._buffer.append(s)
        return len(s)
