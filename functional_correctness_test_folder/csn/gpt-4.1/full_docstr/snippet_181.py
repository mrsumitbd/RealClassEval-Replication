
import os


class BaseLoader:
    '''Base class for File Loaders'''

    def getTextForName(self, query_name):
        '''Return the query text and query type for the given query name.
        Note that file extention is not part of the query name. For example,
        for `query_name='query1'` would return the content of file `query1.rq`
        from the loader's source (assuming such file exists).'''
        # Try common query file extensions
        extensions = ['.rq', '.sparql', '.sql', '.txt']
        for ext in extensions:
            queryFullName = query_name + ext
            text = self._getText(queryFullName)
            if text is not None:
                return text, ext.lstrip('.')
        return None, None

    def _getText(self, queryFullName):
        '''To be implemented by sub-classes.
        Returns None if the file does not exist.'''
        raise NotImplementedError("_getText must be implemented by subclasses")

    def fetchFiles(self):
        '''To be implemented by sub-classes'''
        raise NotImplementedError(
            "fetchFiles must be implemented by subclasses")
