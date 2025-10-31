class RecordLevel:
    '''A class representing the logging level record with name, number and icon.
    Attributes
    ----------
    icon : str
        The icon representing the log level
    name : str
        The name of the log level
    no : int
        The numeric value of the log level
    '''

    def __init__(self, name, no, icon):
        self.name = str(name)
        self.no = int(no)
        self.icon = str(icon)

    def __repr__(self):
        '''Return string representation of RecordLevel.
        Returns
        -------
        str
            Formatted string with name, number and icon
        '''
        return f"{self.__class__.__name__}(name={self.name!r}, no={self.no!r}, icon={self.icon!r})"

    def __format__(self, spec):
        '''Format the RecordLevel instance.
        Parameters
        ----------
        spec : str
            Format specification
        Returns
        -------
        str
            Formatted name according to specification
        '''
        if spec is None:
            spec = ''
        return format(self.name, spec)
