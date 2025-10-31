class UriParam:

    def __init__(self, uri):
        if uri is None:
            raise ValueError("uri cannot be None")
        uri_str = str(uri).strip()
        if not uri_str:
            raise ValueError("uri cannot be empty")
        self.uri = uri_str

    def __repr__(self):
        return f"{self.__class__.__name__}({self.uri!r})"
