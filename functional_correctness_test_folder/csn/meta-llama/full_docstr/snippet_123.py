
from multiprocessing import Manager


class MultiprocessingStringIO:
    '''
    Provide a StringIO-like interface to the multiprocessing ListProxy. The
    multiprocessing ListProxy needs to be instantiated before the flaky plugin
    is configured, so the list is created as a class variable.
    '''
    _list_proxy = Manager().list()

    def getvalue(self):
        '''
        Shadow the StringIO.getvalue method.
        '''
        return ''.join(self._list_proxy)

    def writelines(self, content_list):
        '''
        Shadow the StringIO.writelines method. Ingests a list and
        translates that to a string
        '''
        self._list_proxy.extend(content_list)

    def write(self, content):
        '''
        Shadow the StringIO.write method.
        '''
        self._list_proxy.append(content)
