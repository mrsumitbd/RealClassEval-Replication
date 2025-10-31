class Request:
    """
    A transport request
    @ivar url: The url for the request.
    @type url: str
    @ivar message: The message to be sent in a POST request.
    @type message: str
    @ivar headers: The http headers to be used for the request.
    @type headers: dict
    """

    def __init__(self, url, message=None):
        """
        @param url: The url for the request.
        @type url: str
        @param message: The (optional) message to be send in the request.
        @type message: str
        """
        self.url = url
        self.headers = {}
        self.message = message

    def __str__(self):
        s = []
        s.append('URL:%s' % self.url)
        s.append('HEADERS: %s' % self.headers)
        s.append('MESSAGE:')
        s.append(str(self.message))
        return '\n'.join(s)