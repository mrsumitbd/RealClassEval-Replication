
class RecordLevel:

    def __init__(self, name, no, icon):
        self.name = name
        self.no = no
        self.icon = icon

    def __repr__(self):
        return f"RecordLevel('{self.name}', {self.no}, '{self.icon}')"

    def __format__(self, spec):
        if spec == 'full':
            return f"{self.icon} {self.name} (Level {self.no})"
        elif spec == 'short':
            return f"{self.name} (L{self.no})"
        else:
            return str(self)
