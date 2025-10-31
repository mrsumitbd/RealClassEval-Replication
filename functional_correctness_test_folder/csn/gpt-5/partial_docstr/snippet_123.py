class MultiprocessingStringIO:
    def __init__(self, initial_value=None):
        self._chunks = []
        if initial_value is not None:
            self._chunks.append(str(initial_value))

    def getvalue(self):
        return ''.join(self._chunks)

    def writelines(self, content_list):
        '''
        Shadow the StringIO.writelines method. Ingests a list and
        translates that to a string
        '''
        if content_list is None:
            return
        if isinstance(content_list, (str, bytes)):
            self._chunks.append(content_list.decode() if isinstance(
                content_list, bytes) else content_list)
            return
        try:
            joined = ''.join(str(item) for item in content_list)
        except TypeError:
            raise TypeError(
                "writelines expects an iterable of items to be converted to string")
        self._chunks.append(joined)
