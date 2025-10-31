
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
        self.icon = icon
        self.name = name
        self.no = no

    def __repr__(self):
        '''Return string representation of RecordLevel.
        Returns
        -------
        str
            Formatted string with name, number and icon
        '''
        return f"RecordLevel(name='{self.name}', no={self.no}, icon='{self.icon}')"

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
        return format(self.name, spec)
