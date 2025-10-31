
class CodePageManager:

    def __init__(self, data):
        self.data = data

    @staticmethod
    def get_encoding_name(encoding):
        encoding_names = {
            'cp1252': 'Windows Latin 1',
            'utf-8': 'UTF-8',
            'ascii': 'US-ASCII',
            'iso-8859-1': 'ISO 8859-1',
            'utf-16': 'UTF-16'
        }
        return encoding_names.get(encoding, 'Unknown Encoding')

    def get_encoding_name(self, encoding):
        return CodePageManager.get_encoding_name(encoding)
