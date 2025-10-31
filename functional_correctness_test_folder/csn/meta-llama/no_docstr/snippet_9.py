
class RecordThread:

    def __init__(self, id_, name):
        self.id = id_
        self.name = name

    def __repr__(self):
        return f"RecordThread(id={self.id}, name='{self.name}')"

    def __format__(self, spec):
        if spec == 'id-name':
            return f"{self.id}-{self.name}"
        elif spec == 'name-id':
            return f"{self.name}({self.id})"
        else:
            return str(self)
