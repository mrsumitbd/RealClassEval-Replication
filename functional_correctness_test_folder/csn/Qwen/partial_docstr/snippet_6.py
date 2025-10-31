
class RecordFile:

    def __init__(self, name, path):
        '''Initialize a RecordFile instance.
        Parameters
        ----------
        name : str
            The name of the file
        path : str
            The path to the file
        '''
        self.name = name
        self.path = path

    def __repr__(self):
        return f"RecordFile(name={self.name!r}, path={self.path!r})"

    def __format__(self, spec):
        if spec == 'full':
            return f"{self.path}/{self.name}"
        return f"{self.name}"
