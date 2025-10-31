class RecordFile:

    def __init__(self, name, path):
        from pathlib import Path
        self.name = str(name)
        self.path = Path(path)

    def __repr__(self):
        return f"RecordFile(name={self.name!r}, path={str(self.path)!r})"

    def __format__(self, spec):
        s = spec.strip()
        if not s:
            return str(self)
        key = s.lower()
        if key in ("n", "name"):
            return self.name
        if key in ("p", "path"):
            return str(self.path)
        if key in ("f", "full", "fullpath", "filepath"):
            return str(self.path / self.name)
        return str(self)
