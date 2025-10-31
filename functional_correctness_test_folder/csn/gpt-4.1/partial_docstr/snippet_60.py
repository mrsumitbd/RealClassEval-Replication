
class CodePageManager:
    '''Holds information about all the code pages.
    Information as defined in escpos-printer-db.
    '''

    def __init__(self, data):
        # data is expected to be a list or dict of code page info
        # We'll store by encoding name and by codepage id if available
        self._by_encoding = {}
        self._by_id = {}
        if isinstance(data, dict):
            items = data.items()
        else:
            items = enumerate(data)
        for key, entry in items:
            # entry should have at least 'encoding' key
            encoding = entry.get('encoding') if isinstance(
                entry, dict) else None
            if encoding:
                self._by_encoding[encoding] = entry
            codepage_id = entry.get('id') if isinstance(entry, dict) else None
            if codepage_id is not None:
                self._by_id[codepage_id] = entry

    @staticmethod
    def get_encoding_name(encoding):
        '''Return the normalized encoding name.'''
        # Accepts either a string or a dict with 'encoding' key
        if isinstance(encoding, dict):
            return encoding.get('encoding')
        return encoding

    def get_encoding_data(self, encoding):
        '''Return the encoding data.'''
        name = self.get_encoding_name(encoding)
        return self._by_encoding.get(name)
