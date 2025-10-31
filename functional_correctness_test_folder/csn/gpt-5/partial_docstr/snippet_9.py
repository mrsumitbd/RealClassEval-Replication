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
        if not isinstance(id_, int):
            raise TypeError(f"id_ must be int, got {type(id_).__name__}")
        if not isinstance(name, str):
            raise TypeError(f"name must be str, got {type(name).__name__}")
        self.id = id_
        self.name = name

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id!r}, name={self.name!r})"

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
        return format(self.id, spec)
