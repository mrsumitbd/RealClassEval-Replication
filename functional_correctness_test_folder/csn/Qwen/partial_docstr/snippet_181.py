
import os


class BaseLoader:
    '''Base class for File Loaders'''

    def __init__(self, source_path):
        self.source_path = source_path

    def getTextForName(self, query_name):
        '''Return the query text and query type for the given query name.
        Note that file extention is not part of the query name. For example,
        for `query_name='query1'` would return the content of file `query1.rq`
        from the loader's source (assuming such file exists).'''
        query_full_name = f"{query_name}.rq"
        return self._getText(query_full_name)

    def _getText(self, queryFullName):
        file_path = os.path.join(self.source_path, queryFullName)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return file.read()
        else:
            raise FileNotFoundError(
                f"File {queryFullName} not found in {self.source_path}")

    def fetchFiles(self):
        return [f for f in os.listdir(self.source_path) if os.path.isfile(os.path.join(self.source_path, f))]
