
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
        """Format the RecordFile according to the given spec.

        Supported specs:
            '' or 'repr' : full representation (same as __repr__)
            'n' or 'name' : the file name
            'p' or 'path' : the file path
            'np' or 'full' : name and path separated by a colon
        """
        if not spec or spec == "repr":
            return repr(self)
        if spec in ("n", "name"):
            return self.name
        if spec in ("p", "path"):
            return self.path
        if spec in ("np", "full"):
            return f"{self.name}:{self.path}"
        raise ValueError(f"Unsupported format specifier: {spec!r}")
