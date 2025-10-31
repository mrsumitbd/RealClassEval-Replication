
class CodePageManager:

    def __init__(self, data):
        self.data = data

    @staticmethod
    def get_encoding_name_static(encoding):
        encoding_names = {
            'utf-8': 'UTF-8',
            'utf-16': 'UTF-16',
            'utf-32': 'UTF-32',
            'ascii': 'ASCII',
            'latin1': 'ISO-8859-1',
            'cp1252': 'Windows-1252'
        }
        return encoding_names.get(encoding.lower(), 'Unknown Encoding')

    def get_encoding_name(self, encoding):
        return CodePageManager.get_encoding_name_static(encoding)
