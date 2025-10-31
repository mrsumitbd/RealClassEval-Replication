
class BaseLoader:
    '''Base class for File Loaders'''

    def __init__(self, extensions=None):
        """
        Parameters
        ----------
        extensions : list[str] | None
            List of file extensions (without the leading dot) that this loader
            should consider when looking up queries. If None, defaults to
            ['rq'].
        """
        self.extensions = extensions or ['rq']

    def getTextForName(self, query_name):
        """
        Return the query text and query type for the given query name.
        Note that file extension is not part of the query name. For example,
        for `query_name='query1'` would return the content of file
        `query1.rq` from the loader's source (assuming such file exists).

        Parameters
        ----------
        query_name : str
            The base name of the query file (without extension).

        Returns
        -------
        tuple[str | None, str | None]
            A tuple containing the query text and the query type
            (derived from the file extension). If the query cannot be found,
            returns (None, None).
        """
        for ext in self.extensions:
            full_name = f"{query_name}.{ext}"
            text = self._getText(full_name)
            if text is not None:
                return text, ext
        return None, None

    def _getText(self, queryFullName):
        """
        To be implemented by sub-classes.
        Returns None if the file does not exist.

        Parameters
        ----------
        queryFullName : str
            Full file name including extension.

        Returns
        -------
        str | None
            The content of the file, or None if the file does not exist.
        """
        raise NotImplementedError("Sub-classes must implement _getText")

    def fetchFiles(self):
        """
        To be implemented by sub-classes.
        Should return an iterable of file names (including extensions)
        that the loader can provide.
        """
        raise NotImplementedError("Sub-classes must implement fetchFiles")
