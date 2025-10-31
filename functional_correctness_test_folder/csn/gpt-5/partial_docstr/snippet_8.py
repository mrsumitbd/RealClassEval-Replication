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
        if not isinstance(id_, int):
            raise TypeError("id_ must be an int")
        if not isinstance(name, str):
            raise TypeError("name must be a str")
        self.id = id_
        self.name = name

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
        if spec is None or spec == "":
            return str(self.id)
        return format(self.id, spec)
