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
        '''Initialize a RecordLevel instance.
        Parameters
        ----------
        name : str
            The name of the log level
        no : int
            The numeric value of the log level
        icon : str
            The icon representing the log level
        '''
        if not isinstance(name, str):
            raise TypeError("name must be a str")
        if not isinstance(no, int):
            raise TypeError("no must be an int")
        if not isinstance(icon, str):
            raise TypeError("icon must be a str")
        self.name = name
        self.no = no
        self.icon = icon

    def __repr__(self):
        '''Return string representation of RecordLevel.
        Returns
        -------
        str
            Formatted string with name, number and icon
        '''
        return f"RecordLevel(name={self.name!r}, no={self.no}, icon={self.icon!r})"

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
        if spec is None or spec == "":
            return self.name
        return format(self.name, spec)
