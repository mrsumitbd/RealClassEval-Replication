
class RecordProcess:

    def __init__(self, id_, name):
        self.id_ = id_
        self.name = name

    def __repr__(self):
        return f"RecordProcess(id_={self.id_}, name='{self.name}')"

    def __format__(self, spec):
        if spec == 'short':
            return f"{self.id_}: {self.name}"
        else:
            return self.__repr__()
