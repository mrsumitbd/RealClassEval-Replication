class OBEXResponse:
    """
    Contains the OBEX response received from an OBEX server.

    When an OBEX client sends a request, the OBEX server sends back a response
    code (to indicate whether the request was successful) and a set of response
    headers (to provide other useful information).

    For example, if a client sends a 'Get' request to retrieve a file, the
    client might get a response like this:

        >>> import lightblue
        >>> client = lightblue.obex.OBEXClient("aa:bb:cc:dd:ee:ff", 10)
        >>> response = client.get({"name": "file.txt"}, file("file.txt", "w"))
        >>> print response
        <OBEXResponse reason='OK' code=0x20 (0xa0) headers={'length': 35288}>

    You can get the response code and response headers in different formats:

        >>> print response.reason
        'OK'    # a string description of the response code
        >>> print response.code
        32      # the response code (e.g. this is 0x20)
        >>> print response.headers
        {'length': 35288}   # the headers, with string keys
        >>> print response.rawheaders
        {195: 35288}        # the headers, with raw header ID keys
        >>>

    Note how the 'code' attribute does not have the final bit set - e.g. for
    OK/Success, the response code is 0x20, not 0xA0.

    The lightblue.obex module defines constants for response code values (e.g.
    lightblue.obex.OK, lightblue.obex.FORBIDDEN, etc.).
    """

    def __init__(self, code, rawheaders):
        self.__code = code
        self.__reason = _OBEX_RESPONSES.get(code, 'Unknown response code')
        self.__rawheaders = rawheaders
        self.__headers = None
    code = property(lambda self: self.__code, doc='The response code, without the final bit set.')
    reason = property(lambda self: self.__reason, doc='A string description of the response code.')
    rawheaders = property(lambda self: self.__rawheaders, doc='The response headers, as a dictionary with header ID (unsigned byte) keys.')

    def getheader(self, header, default=None):
        """
        Returns the response header value for the given header, which may
        either be a string (not case-sensitive) or the raw byte
        value of the header ID.

        Returns the specified default value if the header is not present.
        """
        if isinstance(header, str):
            return self.headers.get(header.lower(), default)
        return self.__rawheaders.get(header, default)

    def __getheaders(self):
        if self.__headers is None:
            self.__headers = {}
            for headerid, value in list(self.__rawheaders.items()):
                if headerid in _HEADER_IDS_TO_STRINGS:
                    self.__headers[_HEADER_IDS_TO_STRINGS[headerid]] = value
                else:
                    self.__headers['0x%02x' % headerid] = value
        return self.__headers
    headers = property(__getheaders, doc='The response headers, as a dictionary with string keys.')

    def __repr__(self):
        return "<OBEXResponse reason='%s' code=0x%02x (0x%02x) headers=%s>" % (self.__reason, self.__code, self.__code | 128, str(self.headers))