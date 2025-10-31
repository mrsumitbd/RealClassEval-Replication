
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
        self.id = id_
        self.name = name

    def __repr__(self):
        '''Return string representation of RecordProcess.
        Returns
        -------
        str
            Formatted string with id and name
        '''
        return f"RecordProcess(id={self.id}, name='{self.name}')"

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
        if spec:
            return format(self.id, spec)
        return str(self.id)
