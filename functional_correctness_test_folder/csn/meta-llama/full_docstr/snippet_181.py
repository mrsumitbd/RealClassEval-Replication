
import os


class BaseLoader:
    '''Base class for File Loaders'''

    def __init__(self, file_extension='rq'):
        self.file_extension = file_extension

    def getTextForName(self, query_name):
        '''Return the query text and query type for the given query name.
        Note that file extention is not part of the query name. For example,
        for `query_name='query1'` would return the content of file `query1.rq`
        from the loader's source (assuming such file exists).'''
        query_full_name = f'{query_name}.{self.file_extension}'
        return self._getText(query_full_name)

    def _getText(self, queryFullName):
        '''To be implemented by sub-classes.
        Returns None if the file does not exist.'''
        raise NotImplementedError("Subclass must implement _getText method")

    def fetchFiles(self):
        '''To be implemented by sub-classes'''
        raise NotImplementedError("Subclass must implement fetchFiles method")


class FileSystemLoader(BaseLoader):
    '''A File Loader that loads files from the file system'''

    def __init__(self, directory, file_extension='rq'):
        super().__init__(file_extension)
        self.directory = directory

    def _getText(self, queryFullName):
        file_path = os.path.join(self.directory, queryFullName)
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return None

    def fetchFiles(self):
        try:
            return os.listdir(self.directory)
        except FileNotFoundError:
            return []


# Example usage
if __name__ == "__main__":
    loader = FileSystemLoader('/path/to/queries')
    print(loader.getTextForName('query1'))
    print(loader.fetchFiles())
