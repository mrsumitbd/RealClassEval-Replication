
class RecordProcess:
    def __init__(self, id_, name):
        self.id_ = id_
        self.name = name

    def __repr__(self):
        return f"RecordProcess(id={self.id_!r}, name={self.name!r})"

    def __format__(self, spec):
        if spec == "id":
            return str(self.id_)
        if spec == "name":
            return str(self.name)
        if spec == "full":
            return f"{self.id_}:{self.name}"
        # Default formatting falls back to the repr
        return self.__repr__()
