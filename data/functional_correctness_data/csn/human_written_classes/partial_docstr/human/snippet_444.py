class _ConcatenatedStream:
    """Lazily concatenate zero or more streams into a stream.

    As you read from the concatenated stream, you get characters from
    each stream passed to ``_ConcatenatedStream``, in order.

    **Example**::

        from StringIO import StringIO
        s = _ConcatenatedStream(StringIO("abc"), StringIO("def"))
        assert s.read() == "abcdef"
    """

    def __init__(self, *streams):
        self.streams = list(streams)

    def read(self, n=None):
        """Read at most *n* characters from this stream.

        If *n* is ``None``, return all available characters.
        """
        response = b''
        while len(self.streams) > 0 and (n is None or n > 0):
            txt = self.streams[0].read(n)
            response += txt
            if n is not None:
                n -= len(txt)
            if n is None or n > 0:
                del self.streams[0]
        return response