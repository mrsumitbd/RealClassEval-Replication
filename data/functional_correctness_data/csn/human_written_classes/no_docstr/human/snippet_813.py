import base64

class B64Value:

    def __init__(self, value):
        self.value = value

    @property
    def decode(self):
        return base64.b64decode(self.value)

    def raw(self):
        return self.value

    def __str__(self):
        return self.raw()