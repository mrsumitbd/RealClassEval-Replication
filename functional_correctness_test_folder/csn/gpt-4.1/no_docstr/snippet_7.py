
class RecordLevel:

    def __init__(self, name, no, icon):
        self.name = name
        self.no = no
        self.icon = icon

    def __repr__(self):
        return f"RecordLevel(name={self.name!r}, no={self.no!r}, icon={self.icon!r})"

    def __format__(self, spec):
        if not spec:
            return f"{self.name} ({self.no}) {self.icon}"
        parts = []
        if 'n' in spec:
            parts.append(str(self.name))
        if 'd' in spec:
            parts.append(str(self.no))
        if 'i' in spec:
            parts.append(str(self.icon))
        return " | ".join(parts)
