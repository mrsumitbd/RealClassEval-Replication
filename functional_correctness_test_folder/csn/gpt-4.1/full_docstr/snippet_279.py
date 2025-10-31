
class SearchDumperExt:
    '''Interface for Search dumper extensions.'''

    def dump(self, record, data):
        '''Dump the data.'''
        # Example: Add a marker to indicate data was dumped
        data = data.copy()
        data['_dumped_by'] = self.__class__.__name__
        return data

    def load(self, data, record_cls):
        '''Load the data.
        Reverse the changes made by the dump method.
        '''
        # Remove the marker added in dump
        data = data.copy()
        data.pop('_dumped_by', None)
        return record_cls(**data)
