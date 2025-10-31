
class ShareClass:

    def canonical_uri(self, uri):
        # Normalize the URI: strip spaces, lowercase scheme and host, remove trailing slash
        from urllib.parse import urlparse, urlunparse
        uri = uri.strip()
        parsed = urlparse(uri)
        scheme = parsed.scheme.lower()
        netloc = parsed.netloc.lower()
        path = parsed.path.rstrip('/')
        if not path:
            path = '/'
        new_parsed = parsed._replace(scheme=scheme, netloc=netloc, path=path)
        return urlunparse(new_parsed)

    def service_number(self):
        # Return a fixed service number for this class
        return 42

    @staticmethod
    def magic():
        # Return a static magic string
        return "abracadabra"

    def extract(self, uri):
        # Extract and return the path and query from the URI
        from urllib.parse import urlparse
        parsed = urlparse(uri)
        return {'path': parsed.path, 'query': parsed.query}
