class RecordThread:
    '''A class representing a thread record with ID and name.
    Attributes
    ----------
    id : int
        The thread ID
    name : str
        The thread name
    '''

    def __init__(self, id_, name):
        '''Initialize a RecordThread instance.
        Parameters
        ----------
        id_ : int
            The thread ID
        name : str
            The thread name
        '''
        self.id = int(id_)
        self.name = str(name)

    def __repr__(self):
        '''Return string representation of RecordThread.
        Returns
        -------
        str
            Formatted string with id and name
        '''
        return f"RecordThread(id={self.id!r}, name={self.name!r})"

    def __format__(self, spec):
        '''Format the RecordThread instance.
        Parameters
        ----------
        spec : str
            Format specification
        Returns
        -------
        str
            Formatted ID according to specification
        '''
        if spec is None:
            spec = ""
        return format(self.id, spec)
