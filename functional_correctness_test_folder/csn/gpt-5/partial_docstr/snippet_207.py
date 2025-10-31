class IJavaStreamParser:
    '''
    API of the Java stream parser
    '''

    def run(self):
        '''
        Parses the input stream
        '''
        raise NotImplementedError("Subclasses must implement 'run'")

    def dump(self, content):
        '''
        Dumps to a string the given objects
        '''
        raise NotImplementedError("Subclasses must implement 'dump'")

    def _read_content(self, type_code, block_data, class_desc=None):
        raise NotImplementedError("Subclasses must implement '_read_content'")
