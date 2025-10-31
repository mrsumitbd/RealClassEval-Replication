class NameRedactor:

    def __init__(self, preserve_names=None):
        self.redacted_names = {}
        self.seq = 0
        self.preserve_names = preserve_names or []

    def redact_name(self, name):
        if not name or name in self.preserve_names:
            return name
        redacted_name = self.redacted_names.get(name)
        if not redacted_name:
            redacted_name = f'redacted-{self.seq:04}'
            self.seq += 1
            self.redacted_names[name] = redacted_name
        return redacted_name