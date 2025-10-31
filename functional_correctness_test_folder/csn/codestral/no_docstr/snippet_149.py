
class TorConfigType:

    def parse(self, s):
        return s.strip()

    def validate(self, s, instance, name):
        if not isinstance(s, str):
            raise ValueError(f"{name} must be a string")
        if not s:
            raise ValueError(f"{name} cannot be empty")
