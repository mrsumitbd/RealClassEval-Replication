class UrlPath:
    """
    The  class is a utility for encapsulating and manipulating the path component of a URL, including adding nodes, parsing path strings, and building path strings with optional encoding.
    """

    def __init__(self):
        """
        Initializes the UrlPath object with an empty list of segments and a flag indicating the presence of an end tag.
        """
        self.segments = []
        self.with_end_tag = False

    def add(self, segment):
        """
        Adds a segment to the list of segments in the UrlPath.
        :param segment: str, the segment to add.
        >>> url_path = UrlPath()
        >>> url_path.add('foo')
        >>> url_path.add('bar')

        url_path.segments = ['foo', 'bar']
        """
        if not isinstance(segment, str):
            raise TypeError("segment must be a string")
        self.segments.append(segment)

    def parse(self, path, charset):
        """
        Parses a given path string and populates the list of segments in the UrlPath.
        :param path: str, the path string to parse.
        :param charset: str, the character encoding of the path string.
        >>> url_path = UrlPath()
        >>> url_path.parse('/foo/bar/', 'utf-8')

        url_path.segments = ['foo', 'bar']
        """
        from urllib.parse import unquote

        self.segments = []
        self.with_end_tag = False

        if not path:
            return

        self.with_end_tag = path.endswith('/')

        # Split first to preserve encoded slashes (%2F) within segments
        parts = path.split('/')

        # Remove leading empty (from leading slash)
        while parts and parts[0] == '':
            parts.pop(0)
        # Remove trailing empty (from trailing slash)
        while parts and parts[-1] == '':
            parts.pop()

        # Decode each non-empty segment
        decoded = []
        for p in parts:
            if p == '':
                # ignore empty segments from consecutive slashes
                continue
            decoded.append(unquote(p, encoding=charset, errors='strict'))

        self.segments = decoded

    @staticmethod
    def fix_path(path):
        """
        Fixes the given path string by removing leading and trailing slashes.
        :param path: str, the path string to fix.
        :return: str, the fixed path string.
        >>> url_path = UrlPath()
        >>> url_path.fix_path('/foo/bar/')
        'foo/bar'

        """
        if path is None:
            return ''
        return path.strip('/')
