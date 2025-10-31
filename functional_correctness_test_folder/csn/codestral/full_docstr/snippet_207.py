
class IJavaStreamParser:
    '''
    API of the Java stream parser
    '''

    def run(self):
        '''
        Parses the input stream
        '''
        pass

    def dump(self, content):
        '''
        Dumps to a string the given objects
        '''
        pass

    def _read_content(self, type_code, block_data, class_desc=None):
        '''
        Parses the next content. Use with care (use only in a transformer)
        '''
        pass
