
class RecordFile:

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def __repr__(self):
        return f"RecordFile(name='{self.name}', path='{self.path}')"

    def __format__(self, spec):
        if spec == 'full':
            return f"{self.path}/{self.name}"
        elif spec == 'short':
            return self.name
        else:
            raise ValueError(
                "Invalid format specifier. Use 'full' or 'short'.")
