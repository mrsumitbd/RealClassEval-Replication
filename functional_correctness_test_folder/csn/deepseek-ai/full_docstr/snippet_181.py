
class BaseLoader:
    '''Base class for File Loaders'''

    def getTextForName(self, query_name):
        '''Return the query text and query type for the given query name.
        Note that file extention is not part of the query name. For example,
        for `query_name='query1'` would return the content of file `query1.rq`
        from the loader's source (assuming such file exists).'''
        query_full_name = f"{query_name}.rq"
        return self._getText(query_full_name)

    def _getText(self, queryFullName):
        '''To be implemented by sub-classes.
        Returns None if the file does not exist.'''
        raise NotImplementedError("Subclasses must implement this method")

    def fetchFiles(self):
        '''To be implemented by sub-classes'''
        raise NotImplementedError("Subclasses must implement this method")
