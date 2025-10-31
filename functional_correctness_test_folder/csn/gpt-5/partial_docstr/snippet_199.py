class UriParam:

    def __init__(self, uri):
        '''
        Initialize the UriParam value
        :param uri: the uri value to wrap
        '''
        if uri is None:
            raise ValueError("uri cannot be None")
        self._uri = str(uri)

    def __repr__(self):
        '''
        The official string representation for the URI
        :return: the string representation for the URI
        '''
        return self._uri
