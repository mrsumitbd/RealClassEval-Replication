class RecordFile:
    '''A class representing a file record with name and path.
    Attributes
    ----------
    name : str
        The name of the file
    path : str
        The path to the file
    '''

    def __init__(self, name, path):
        '''Initialize a RecordFile instance.
        Parameters
        ----------
        name : str
            The name of the file
        path : str
            The path to the file
        '''
        if not isinstance(name, str):
            raise TypeError("name must be a str")
        if not isinstance(path, str):
            raise TypeError("path must be a str")
        self.name = name
        self.path = path

    def __repr__(self):
        '''Return string representation of RecordFile.
        Returns
        -------
        str
            Formatted string with name and path
        '''
        return f"{self.__class__.__name__}(name={self.name!r}, path={self.path!r})"

    def __format__(self, spec):
        '''Format the RecordFile instance.
        Parameters
        ----------
        spec : str
            Format specification
        Returns
        -------
        str
            Formatted name according to specification
        '''
        if not isinstance(spec, str):
            raise TypeError("spec must be a str")
        return format(self.name, spec)
