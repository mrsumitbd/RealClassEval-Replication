class FakeResponse:

    def __init__(self, method, headers):
        self._method = method
        self.msg = FakeHeaders(headers)
        self.closed = False

    def close(self):
        self.closed = True

    def isclosed(self):
        return self.closed