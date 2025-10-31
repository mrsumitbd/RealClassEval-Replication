
class CodePageManager:
    '''Holds information about all the code pages.
    Information as defined in escpos-printer-db.
    '''

    def __init__(self, data):
        self.data = data

    @staticmethod
    def get_encoding_name(encoding):
        # Assuming encoding is a dictionary with 'code' as key and 'name' as value
        for code, name in encoding.items():
            if code == encoding:
                return name
        return None

    def get_encoding_name(self, encoding_code):
        '''Return the encoding data.'''
        return self.data.get(encoding_code, None)
