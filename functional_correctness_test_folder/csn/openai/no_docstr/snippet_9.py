
class RecordThread:
    def __init__(self, id_, name):
        self.id = id_
        self.name = name

    def __repr__(self):
        return f"RecordThread(id={self.id!r}, name={self.name!r})"

    def __format__(self, spec):
        # Default formatting: id followed by name
        if not spec:
            return f"{self.id} {self.name}"
        # If the spec is "name", return only the name
        if spec == "name":
            return f"{self.name}"
        # If the spec is "id", return only the id (formatted with the spec)
        if spec == "id":
            return f"{self.id}"
        # Try to format the id with the given spec (e.g., numeric formatting)
        try:
            return format(self.id, spec)
        except Exception:
            # Fallback to the default representation
            return f"{self.id} {self.name}"
