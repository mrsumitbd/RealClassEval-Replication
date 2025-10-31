class RecordThread:

    def __init__(self, id_, name):
        self.id = id_
        self.name = name

    def __repr__(self):
        return f"RecordThread(id_={self.id!r}, name={self.name!r})"

    def __format__(self, spec):
        if spec is None:
            spec = ""
        if spec == "" or spec in ("r", "repr"):
            return str(self)
        if spec in ("n", "name"):
            return format(self.name, "")
        if spec.startswith("n:") or spec.startswith("name:"):
            _, inner = spec.split(":", 1)
            return format(self.name, inner)
        if spec in ("i", "id"):
            return format(self.id, "")
        if spec.startswith("i:") or spec.startswith("id:"):
            _, inner = spec.split(":", 1)
            return format(self.id, inner)
        return format(str(self), spec)
