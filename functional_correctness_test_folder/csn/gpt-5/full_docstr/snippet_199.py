class UriParam:
    '''Represents a URI value as a parameter to a SPARQL query'''

    def __init__(self, uri):
        '''
        Initialize the UriParam value
        :param uri: the uri value to wrap
        '''
        if not isinstance(uri, str):
            raise TypeError("uri must be a string")
        s = uri.strip()
        if s.startswith("<") and s.endswith(">"):
            s = s[1:-1].strip()
        if not s:
            raise ValueError("uri cannot be empty")
        self._uri = s

    def __repr__(self):
        '''
        The official string representation for the URI
        :return: the string representation for the URI
        '''
        return f"<{self._uri}>"
