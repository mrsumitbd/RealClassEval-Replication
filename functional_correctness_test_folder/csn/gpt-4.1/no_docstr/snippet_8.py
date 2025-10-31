
class RecordProcess:

    def __init__(self, id_, name):
        self.id_ = id_
        self.name = name

    def __repr__(self):
        return f"RecordProcess(id_={self.id_!r}, name={self.name!r})"

    def __format__(self, spec):
        if not spec:
            return f"{self.id_}:{self.name}"
        elif spec == "id":
            return f"{self.id_}"
        elif spec == "name":
            return f"{self.name}"
        else:
            raise ValueError(f"Unknown format specifier: {spec}")
