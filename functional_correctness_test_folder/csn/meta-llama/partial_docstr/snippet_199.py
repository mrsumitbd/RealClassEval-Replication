
class UriParam:

    def __init__(self, uri):
        '''
        Initialize the UriParam value
        :param uri: the uri value to wrap
        '''
        self.uri = uri

    def __repr__(self):
        '''
        The official string representation for the URI
        :return: the string representation for the URI
        '''
        return f"UriParam('{self.uri}')"
