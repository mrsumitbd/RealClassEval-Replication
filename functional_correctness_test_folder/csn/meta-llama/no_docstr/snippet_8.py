
class RecordProcess:

    def __init__(self, id_, name):
        self.id = id_
        self.name = name

    def __repr__(self):
        return f"RecordProcess(id={self.id}, name='{self.name}')"

    def __format__(self, spec):
        if spec == 'short':
            return f"{self.id}:{self.name}"
        elif spec == 'long':
            return f"Process ID: {self.id}, Process Name: {self.name}"
        else:
            return str(self)
