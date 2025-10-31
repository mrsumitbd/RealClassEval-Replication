
import urllib.parse


class UriParam:
    """
    A simple wrapper around urllib.parse.urlparse that stores the parsed
    components of a URI and provides a convenient representation.
    """

    def __init__(self, uri: str):
        """
        Parse the given URI and store its components.

        Parameters
        ----------
        uri : str
            The URI to parse.
        """
        if not isinstance(uri, str):
            raise TypeError(f"uri must be a string, got {type(uri).__name__}")

        self._parsed = urllib.parse.urlparse(uri)

        # Individual components
        self.scheme = self._parsed.scheme
        self.netloc = self._parsed.netloc
        self.path = self._parsed.path
        self.params = self._parsed.params
        self.query = self._parsed.query
        self.fragment = self._parsed.fragment

        # Query parameters as a dict of lists
        self.query_params = urllib.parse.parse_qs(
            self.query, keep_blank_values=True)

    def __repr__(self) -> str:
        """
        Return a string representation of the UriParam instance.
        """
        return (
            f"{self.__class__.__name__}("
            f"scheme={self.scheme!r}, "
            f"netloc={self.netloc!r}, "
            f"path={self.path!r}, "
            f"params={self.params!r}, "
            f"query={self.query!r}, "
            f"fragment={self.fragment!r})"
        )
