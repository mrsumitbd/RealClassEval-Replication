
class RecordFile:

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def __repr__(self):
        return f"RecordFile(name={self.name!r}, path={self.path!r})"

    def __format__(self, spec):
        if spec == 'full':
            return f"{self.path}/{self.name}"
        elif spec == 'name':
            return self.name
        elif spec == 'path':
            return self.path
        else:
            return f"RecordFile({self.name}, {self.path})"
