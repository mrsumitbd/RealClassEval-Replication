
class MultiprocessingStringIO:
    '''
    Provide a StringIO-like interface to the multiprocessing ListProxy. The
    multiprocessing ListProxy needs to be instantiated before the flaky plugin
    is configured, so the list is created as a class variable.
    '''
    _list = []

    def __init__(self, list_proxy=None):
        if list_proxy is not None:
            self._list = list_proxy

    def getvalue(self):
        '''
        Shadow the StringIO.getvalue method.
        '''
        return ''.join(self._list)

    def writelines(self, content_list):
        '''
        Shadow the StringIO.writelines method. Ingests a list and
        translates that to a string
        '''
        for line in content_list:
            self._list.append(str(line))

    def write(self, content):
        '''
        Shadow the StringIO.write method.
        '''
        self._list.append(str(content))
