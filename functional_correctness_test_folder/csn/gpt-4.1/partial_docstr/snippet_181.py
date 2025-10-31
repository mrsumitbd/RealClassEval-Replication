
import os


class BaseLoader:
    '''Base class for File Loaders'''

    def __init__(self, directory='.'):
        self.directory = directory
        self._files = None  # cache for file list

    def getTextForName(self, query_name):
        '''Return the query text and query type for the given query name.
        Note that file extention is not part of the query name. For example,
        for `query_name='query1'` would return the content of file `query1.rq`
        from the loader's source (assuming such file exists).'''
        files = self.fetchFiles()
        for fname in files:
            base, ext = os.path.splitext(fname)
            if base == query_name:
                text = self._getText(fname)
                query_type = ext[1:] if ext.startswith('.') else ext
                return text, query_type
        raise FileNotFoundError(f"No file found for query name '{query_name}'")

    def _getText(self, queryFullName):
        path = os.path.join(self.directory, queryFullName)
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def fetchFiles(self):
        if self._files is None:
            self._files = [f for f in os.listdir(self.directory)
                           if os.path.isfile(os.path.join(self.directory, f))]
        return self._files
