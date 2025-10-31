
import re
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode


class ShareClass:
    """
    A utility class for working with URIs.
    """

    def canonical_uri(self, uri: str) -> str:
        """
        Return a canonical form of the given URI:
        * scheme and host are lower‑cased
        * default ports (80 for http, 443 for https) are removed
        * query parameters are sorted by key
        * fragments are stripped
        """
        if not uri:
            return ""

        parsed = urlparse(uri)

        # Lower‑case scheme and netloc
        scheme = parsed.scheme.lower()
        netloc = parsed.netloc.lower()

        # Remove default ports
        if ":" in netloc:
            host, port = netloc.split(":", 1)
            if (scheme == "http" and port == "80") or (scheme == "https" and port == "443"):
                netloc = host

        # Sort query parameters
        query = urlencode(
            sorted(parse_qsl(parsed.query, keep_blank_values=True)))

        # Rebuild the URI without fragment
        canonical = urlunparse(
            (scheme, netloc, parsed.path, parsed.params, query, ""))
        return canonical

    def service_number(self) -> int:
        """
        Return a service number extracted from the instance's URI.
        The service number is defined as the first integer found in the path.
        If no integer is found, return 0.
        """
        if not hasattr(self, "_uri"):
            return 0

        match = re.search(r"/(\d+)", self._uri)
        return int(match.group(1)) if match else 0

    @staticmethod
    def magic() -> int:
        """
        Return a magic constant used by the class.
        """
        return 42

    def extract(self, uri: str) -> dict:
        """
        Parse the given URI and return its components as a dictionary.
        """
        if not uri:
            return {}

        parsed = urlparse(uri)
        return {
            "scheme": parsed.scheme,
            "netloc": parsed.netloc,
            "path": parsed.path,
            "params": parsed.params,
            "query": parsed.query,
            "fragment": parsed.fragment,
        }
