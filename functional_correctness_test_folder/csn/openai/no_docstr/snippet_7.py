
class RecordLevel:
    def __init__(self, name, no, icon):
        self.name = name
        self.no = no
        self.icon = icon

    def __repr__(self):
        return f"RecordLevel(name={self.name!r}, no={self.no!r}, icon={self.icon!r})"

    def __format__(self, spec):
        if not spec:
            return repr(self)

        spec = spec.lower()
        if spec in ("n", "name"):
            return str(self.name)
        if spec in ("i", "icon"):
            return str(self.icon)
        if spec in ("o", "no"):
            return str(self.no)
        if spec == "repr":
            return repr(self)

        raise ValueError(f"Unknown format specifier {spec!r}")
