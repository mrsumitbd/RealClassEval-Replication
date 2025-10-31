
class RecordLevel:

    def __init__(self, name, no, icon):
        self.name = name
        self.no = no
        self.icon = icon

    def __repr__(self):
        return f"RecordLevel(name={self.name!r}, no={self.no!r}, icon={self.icon!r})"

    def __format__(self, spec):
        if spec == 'name':
            return self.name
        elif spec == 'no':
            return str(self.no)
        elif spec == 'icon':
            return self.icon
        else:
            return f"RecordLevel(name={self.name!r}, no={self.no!r}, icon={self.icon!r})"
