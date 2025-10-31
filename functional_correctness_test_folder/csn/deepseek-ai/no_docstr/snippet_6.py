
class RecordFile:

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def __repr__(self):
        return f"RecordFile(name='{self.name}', path='{self.path}')"

    def __format__(self, spec):
        if spec == 'n':
            return self.name
        elif spec == 'p':
            return self.path
        elif spec == 'np':
            return f"{self.name} ({self.path})"
        else:
            return str(self)
