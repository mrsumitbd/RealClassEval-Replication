class MetPyChecker:
    name = "metpy-checker"
    version = "0.1.0"

    def __init__(self, tree):
        self.tree = tree
        self._errors = []

    def run(self):
        for err in self._errors:
            yield err

    def error(self, err):
        # Normalize different error formats to (line, col, msg, type)
        if isinstance(err, tuple):
            if len(err) == 4:
                line, col, msg, typ = err
                self._errors.append((int(line), int(col), str(msg), typ))
                return
            if len(err) == 3:
                line, col, msg = err
                self._errors.append(
                    (int(line), int(col), str(msg), type(self)))
                return
        # Fallback: store as a generic error on line 1, col 0 with stringified message
        self._errors.append((1, 0, str(err), type(self)))
