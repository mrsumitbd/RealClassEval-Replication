
class CodePageManager:
    '''Holds information about all the code pages.
    Information as defined in escpos-printer-db.
    '''

    def __init__(self, data):
        '''Initialize code page manager.'''
        self.data = data
        # Build a mapping from encoding names and aliases to canonical names
        self._encoding_map = {}
        for codepage in data:
            name = codepage.get('encoding')
            if name:
                self._encoding_map[name.lower()] = name
            aliases = codepage.get('aliases', [])
            for alias in aliases:
                self._encoding_map[alias.lower()] = name

    @staticmethod
    def get_encoding_name(encoding):
        '''Get encoding name.
        .. todo:: Resolve the encoding alias.
        '''
        # For static method, just return the lowercased encoding name
        if encoding is None:
            return None
        return str(encoding).lower()

    def get_encoding_name(self, encoding):
        '''Return the encoding data.'''
        if encoding is None:
            return None
        key = str(encoding).lower()
        return self._encoding_map.get(key)
