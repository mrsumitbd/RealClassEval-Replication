
class TorConfigType:

    def parse(self, s):
        return s

    def validate(self, s, instance, name):
        if not isinstance(instance, str):
            raise ValueError(f"{name} must be a string")
