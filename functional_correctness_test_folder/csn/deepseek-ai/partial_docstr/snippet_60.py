
class CodePageManager:
    '''Holds information about all the code pages.
    Information as defined in escpos-printer-db.
    '''

    def __init__(self, data):
        self.data = data

    @staticmethod
    def get_encoding_name(encoding):
        '''Return the encoding data.'''
        return encoding

    def get_encoding(self, encoding):
        '''Return the encoding data.'''
        return self.data.get(encoding, None)
