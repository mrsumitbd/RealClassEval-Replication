
class TorConfigType:

    def parse(self, s):
        if not isinstance(s, str):
            raise ValueError("Input must be a string")
        return s.strip()

    def validate(self, s, instance, name):
        if not isinstance(s, str):
            raise TypeError(f"{name} must be a string")
        if not s:
            raise ValueError(f"{name} cannot be an empty string")
