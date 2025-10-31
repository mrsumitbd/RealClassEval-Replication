class _XMLDTDFilter:
    """Lazily remove all XML DTDs from a stream.

    All substrings matching the regular expression <?[^>]*> are
    removed in their entirety from the stream. No regular expressions
    are used, however, so everything still streams properly.

    **Example**::

        from StringIO import StringIO
        s = _XMLDTDFilter("<?xml abcd><element><?xml ...></element>")
        assert s.read() == "<element></element>"
    """

    def __init__(self, stream):
        self.stream = stream

    def read(self, n=None):
        """Read at most *n* characters from this stream.

        If *n* is ``None``, return all available characters.
        """
        response = b''
        while n is None or n > 0:
            c = self.stream.read(1)
            if c == b'':
                break
            if c == b'<':
                c += self.stream.read(1)
                if c == b'<?':
                    while True:
                        q = self.stream.read(1)
                        if q == b'>':
                            break
                else:
                    response += c
                    if n is not None:
                        n -= len(c)
            else:
                response += c
                if n is not None:
                    n -= 1
        return response