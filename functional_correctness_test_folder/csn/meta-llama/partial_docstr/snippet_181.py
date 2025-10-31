
import os


class BaseLoader:
    '''Base class for File Loaders'''

    def __init__(self, directory):
        """
        Initialize the BaseLoader with a directory path.

        :param directory: The directory path to load files from.
        """
        self.directory = directory

    def getTextForName(self, query_name):
        '''Return the query text and query type for the given query name.
        Note that file extention is not part of the query name. For example,
        for `query_name='query1'` would return the content of file `query1.rq`
        from the loader's source (assuming such file exists).'''
        for file in self.fetchFiles():
            filename, file_extension = os.path.splitext(file)
            if filename == query_name:
                return self._getText(os.path.join(self.directory, file))
        return None

    def _getText(self, queryFullName):
        try:
            with open(queryFullName, 'r') as file:
                query_text = file.read()
                _, file_extension = os.path.splitext(queryFullName)
                # Remove the dot from the extension
                query_type = file_extension[1:]
                return query_text, query_type
        except FileNotFoundError:
            return None

    def fetchFiles(self):
        try:
            return os.listdir(self.directory)
        except FileNotFoundError:
            return []
