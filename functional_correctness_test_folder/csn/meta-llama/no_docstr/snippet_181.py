
import os


class BaseLoader:
    def __init__(self, root_dir):
        """
        Initialize the BaseLoader with a root directory.

        :param root_dir: The root directory to load files from.
        """
        self.root_dir = root_dir

    def getTextForName(self, query_name):
        """
        Get the text for a given query name.

        :param query_name: The name to query for.
        :return: The text associated with the query name.
        """
        query_full_name = os.path.join(self.root_dir, query_name)
        return self._getText(query_full_name)

    def _getText(self, queryFullName):
        """
        Get the text from a file.

        :param queryFullName: The full path to the file.
        :return: The text in the file.
        """
        try:
            with open(queryFullName, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return None

    def fetchFiles(self):
        """
        Fetch a list of files in the root directory.

        :return: A list of file names in the root directory.
        """
        return [f for f in os.listdir(self.root_dir) if os.path.isfile(os.path.join(self.root_dir, f))]


# Example usage:
if __name__ == "__main__":
    loader = BaseLoader('/path/to/your/directory')
    print(loader.fetchFiles())
    print(loader.getTextForName('example.txt'))
