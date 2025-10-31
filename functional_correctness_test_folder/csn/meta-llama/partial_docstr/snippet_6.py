
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
        return f"RecordFile('{self.name}', '{self.path}')"

    def __format__(self, spec):
        if spec == 'full_path':
            return f"{self.path}/{self.name}"
        elif spec == 'name_only':
            return self.name
        else:
            return str(self)
