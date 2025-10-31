
import os


class BaseLoader:
    """
    A simple loader that reads text files from a directory.
    Each file is identified by its base name (without extension).
    """

    def __init__(self, directory, file_extension=".txt"):
        """
        Parameters
        ----------
        directory : str
            Path to the directory containing the text files.
        file_extension : str, optional
            Extension of the files to load (default: ".txt").
        """
        self.directory = os.path.abspath(directory)
        self.file_extension = file_extension
        self._files = None          # mapping: name -> full path
        self._cache = {}            # mapping: name -> file content

    def fetchFiles(self):
        """
        Scan the directory for files with the specified extension and
        build a mapping from file base name to full path.

        Returns
        -------
        dict
            Mapping of file names (without extension) to absolute file paths.
        """
        if self._files is None:
            self._files = {}
            for root, _, files in os.walk(self.directory):
                for fname in files:
                    if fname.lower().endswith(self.file_extension):
                        name = os.path.splitext(fname)[0]
                        full_path = os.path.join(root, fname)
                        self._files[name] = full_path
        return self._files

    def _getText(self, queryFullName):
        """
        Read the content of a file.

        Parameters
        ----------
        queryFullName : str
            Absolute path to the file.

        Returns
        -------
        str
            The file's content.

        Raises
        ------
        FileNotFoundError
            If the file does not exist.
        """
        if not os.path.isfile(queryFullName):
            raise FileNotFoundError(f"File not found: {queryFullName}")
        with open(queryFullName, "r", encoding="utf-8") as f:
            return f.read()

    def getTextForName(self, query_name):
        """
        Retrieve the text content for a given file name.

        Parameters
        ----------
        query_name : str
            The base name of the file (without extension).

        Returns
        -------
        str
            The file's content.

        Raises
        ------
        KeyError
            If the name is not found among the loaded files.
        """
        if query_name in self._cache:
            return self._cache[query_name]

        files = self.fetchFiles()
        if query_name not in files:
            raise KeyError(
                f"Name '{query_name}' not found in directory '{self.directory}'")

        full_path = files[query_name]
        text = self._getText(full_path)
        self._cache[query_name] = text
        return text
