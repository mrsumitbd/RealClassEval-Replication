
class RecordFile:

    def __init__(self, name, path):

        self.name = name
        self.path = path

    def __repr__(self):

        return f"RecordFile(name='{self.name}', path='{self.path}')"

    def __format__(self, spec):

        if spec == "name":
            return self.name
        elif spec == "path":
            return self.path
        else:
            return repr(self)
