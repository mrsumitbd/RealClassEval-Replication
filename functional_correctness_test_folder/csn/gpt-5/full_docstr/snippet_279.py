class SearchDumperExt:
    '''Interface for Search dumper extensions.'''

    def dump(self, record, data):
        '''Dump the data.'''
        raise NotImplementedError("Subclasses must implement dump().")

    def load(self, data, record_cls):
        '''Load the data.
        Reverse the changes made by the dump method.
        '''
        raise NotImplementedError("Subclasses must implement load().")
