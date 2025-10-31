
from urllib.parse import urlparse


class UriParam:

    def __init__(self, uri):
        self.uri = uri
        self.parsed_uri = urlparse(uri)

    def __repr__(self):
        return f"UriParam('{self.uri}')"
