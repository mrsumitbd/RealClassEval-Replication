class RecordProcess:
    '''A class representing a process record with ID and name.
    Attributes
    ----------
    id : int
        The process ID
    name : str
        The process name
    '''

    def __init__(self, id_, name):
        '''Initialize a RecordProcess instance.
        Parameters
        ----------
        id_ : int
            The process ID
        name : str
            The process name
        '''
        self.id = int(id_)
        self.name = str(name)

    def __repr__(self):
        return f"RecordProcess(id={self.id!r}, name={self.name!r})"

    def __format__(self, spec):
        '''Format the RecordProcess instance.
        Parameters
        ----------
        spec : str
            Format specification
        Returns
        -------
        str
            Formatted ID according to specification
        '''
        return format(self.id, spec)
