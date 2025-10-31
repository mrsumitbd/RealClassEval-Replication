
class CodePageManager:
    '''Holds information about all the code pages.
    Information as defined in escpos-printer-db.
    '''

    def __init__(self, data):
        '''Initialize code page manager.'''
        self.data = data

    @staticmethod
    def get_encoding_name(encoding):
        '''Get encoding name.
        .. todo:: Resolve the encoding alias.
        '''
        # For simplicity, we assume that the encoding name is the same as the encoding.
        # In a real-world scenario, you would need to implement a more sophisticated method to resolve the encoding alias.
        return encoding

    def get_code_page_data(self, encoding):
        '''Return the encoding data.'''
        encoding_name = self.get_encoding_name(encoding)
        return self.data.get(encoding_name)
