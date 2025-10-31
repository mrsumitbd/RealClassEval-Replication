class RecordProcess:

    def __init__(self, id_, name):
        self.id_ = id_
        self.name = name

    def __repr__(self):
        return f"RecordProcess(id_={self.id_!r}, name={self.name!r})"

    def __format__(self, spec):
        if not spec:
            return f"{self.name}({self.id_})"
        if spec in ("r", "repr"):
            return repr(self)
        if spec.startswith("name"):
            sub = spec[4:]
            if sub.startswith(":"):
                sub = sub[1:]
            return format(self.name, sub)
        if spec.startswith("id"):
            sub = spec[2:]
            if sub.startswith(":"):
                sub = sub[1:]
            return format(self.id_, sub)
        return format(f"{self.name}({self.id_})", spec)
