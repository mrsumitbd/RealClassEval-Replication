
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
        if not spec:
            return f"{self.name} at {self.path}"
        elif spec == "name":
            return self.name
        elif spec == "path":
            return self.path
        else:
            return format(str(self), spec)
