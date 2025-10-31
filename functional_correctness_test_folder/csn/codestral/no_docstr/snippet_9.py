
class RecordThread:

    def __init__(self, id_, name):
        self.id_ = id_
        self.name = name

    def __repr__(self):
        return f"RecordThread(id_={self.id_}, name='{self.name}')"

    def __format__(self, spec):
        if spec == "id":
            return str(self.id_)
        elif spec == "name":
            return self.name
        else:
            return repr(self)
