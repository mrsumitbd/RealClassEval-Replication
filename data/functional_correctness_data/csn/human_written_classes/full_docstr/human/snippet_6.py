class RecordFile:
    """A class representing a file record with name and path.

    Attributes
    ----------
    name : str
        The name of the file
    path : str
        The path to the file
    """
    __slots__ = ('name', 'path')

    def __init__(self, name, path):
        """Initialize a RecordFile instance.

        Parameters
        ----------
        name : str
            The name of the file
        path : str
            The path to the file
        """
        self.name = name
        self.path = path

    def __repr__(self):
        """Return string representation of RecordFile.

        Returns
        -------
        str
            Formatted string with name and path
        """
        return '(name=%r, path=%r)' % (self.name, self.path)

    def __format__(self, spec):
        """Format the RecordFile instance.

        Parameters
        ----------
        spec : str
            Format specification

        Returns
        -------
        str
            Formatted name according to specification
        """
        return self.name.__format__(spec)