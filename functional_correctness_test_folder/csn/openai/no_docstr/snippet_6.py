
class RecordFile:
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def __repr__(self):
        return f"RecordFile(name={self.name!r}, path={self.path!r})"

    def __format__(self, spec):
        """
        Format specifiers:
            ''  -> repr(self)
            'n' -> self.name
            'p' -> self.path
        Any other spec falls back to repr.
        """
        if spec == "n":
            return self.name
        if spec == "p":
            return self.path
        return repr(self)
