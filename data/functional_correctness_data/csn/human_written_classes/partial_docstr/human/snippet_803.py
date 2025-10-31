class Reply:
    """
    A transport reply
    @ivar code: The http code returned.
    @type code: int
    @ivar message: The message to be sent in a POST request.
    @type message: str
    @ivar headers: The http headers to be used for the request.
    @type headers: dict
    """

    def __init__(self, code, headers, message):
        """
        @param code: The http code returned.
        @type code: int
        @param headers: The http returned headers.
        @type headers: dict
        @param message: The (optional) reply message received.
        @type message: str
        """
        self.code = code
        self.headers = headers
        self.message = message

    def __str__(self):
        s = []
        s.append('CODE: %s' % self.code)
        s.append('HEADERS: %s' % self.headers)
        s.append('MESSAGE:')
        s.append(str(self.message))
        return '\n'.join(s)