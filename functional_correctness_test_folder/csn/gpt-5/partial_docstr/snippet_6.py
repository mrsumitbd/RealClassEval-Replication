import os


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
        if not isinstance(name, str):
            raise TypeError("name must be a str")
        if not isinstance(path, str):
            raise TypeError("path must be a str")
        self.name = name
        self.path = path

    def __repr__(self):
        return f"RecordFile(name={self.name!r}, path={self.path!r})"

    def __format__(self, spec):
        if not spec:
            return repr(self)
        key = spec.lower()
        if key in ("n", "name"):
            return self.name
        if key in ("p", "path"):
            return self.path
        if key in ("f", "full", "filepath", "fullpath"):
            return os.path.normpath(os.path.join(self.path, self.name))
        return format(repr(self), spec)
