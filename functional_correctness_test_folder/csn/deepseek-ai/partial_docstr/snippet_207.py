
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
        Reads content based on type code, block data, and optional class descriptor
        '''
        pass
