
class CodePageManager:
    '''Holds information about all the code pages.
    Information as defined in escpos-printer-db.
    '''

    def __init__(self, data):
        """
        Initialize the manager with a dictionary of code page data.
        The keys are expected to be canonical encoding names.
        """
        # Store a case‑insensitive copy of the data
        self._data = {k.lower(): v for k, v in data.items()}

    @staticmethod
    def get_encoding_name(encoding):
        """
        Return the canonical encoding name for a given alias.
        """
        # Common aliases mapping to canonical names
        alias_map = {
            'cp437': '437',
            '437': '437',
            'cp850': '850',
            '850': '850',
            'cp852': '852',
            '852': '852',
            'cp855': '855',
            '855': '855',
            'cp857': '857',
            '857': '857',
            'cp860': '860',
            '860': '860',
            'cp861': '861',
            '861': '861',
            'cp862': '862',
            '862': '862',
            'cp863': '863',
            '863': '863',
            'cp864': '864',
            '864': '864',
            'cp865': '865',
            '865': '865',
            'cp866': '866',
            '866': '866',
            'cp869': '869',
            '869': '869',
            'cp1252': '1252',
            'windows-1252': '1252',
            '1252': '1252',
            'utf-8': 'utf8',
            'utf8': 'utf8',
            'latin1': 'latin1',
            'iso8859-1': 'latin1',
            'iso8859-15': 'latin9',
            'latin9': 'latin9',
        }
        key = encoding.lower()
        return alias_map.get(key, key)

    def get_encoding_name(self, encoding):
        """
        Return the encoding data for the given encoding.
        Raises KeyError if the encoding is not known.
        """
        # Try the raw key first
        key = encoding.lower()
        if key in self._data:
            return self._data[key]

        # Try canonical name mapping
        canonical = self.get_encoding_name(encoding)
        if canonical in self._data:
            return self._data[canonical]

        # Not found
        raise KeyError(f"Encoding '{encoding}' not found in code page data.")
