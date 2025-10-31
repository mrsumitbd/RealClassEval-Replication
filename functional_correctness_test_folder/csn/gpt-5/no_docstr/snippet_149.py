class TorConfigType:
    def parse(self, s):
        if s is None:
            return None
        if isinstance(s, bytes):
            try:
                s = s.decode("utf-8")
            except Exception:
                s = s.decode("utf-8", errors="replace")
        elif not isinstance(s, str):
            s = str(s)
        return s.strip()

    def validate(self, s, instance, name):
        value = self.parse(s)
        if value is None:
            return True
        if "\x00" in value:
            raise ValueError(f"Invalid value for {name}: contains NUL byte")
        if value == "":
            raise ValueError(f"Invalid value for {name}: empty string")
        return True
