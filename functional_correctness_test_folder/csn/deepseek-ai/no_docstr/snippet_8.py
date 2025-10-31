
class RecordProcess:

    def __init__(self, id_, name):
        self.id_ = id_
        self.name = name

    def __repr__(self):
        return f"RecordProcess(id_={self.id_!r}, name={self.name!r})"

    def __format__(self, spec):
        if spec == 'id':
            return str(self.id_)
        elif spec == 'name':
            return self.name
        elif spec == 'full':
            return f"{self.id_}: {self.name}"
        else:
            return str(self)
