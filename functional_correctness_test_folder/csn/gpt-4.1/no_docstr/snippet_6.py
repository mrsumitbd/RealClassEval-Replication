
class RecordFile:

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def __repr__(self):
        return f"RecordFile(name={self.name!r}, path={self.path!r})"

    def __format__(self, spec):
        if not spec:
            return f"{self.name} at {self.path}"
        elif spec == "name":
            return f"{self.name}"
        elif spec == "path":
            return f"{self.path}"
        else:
            raise ValueError(f"Unknown format specifier: {spec}")
