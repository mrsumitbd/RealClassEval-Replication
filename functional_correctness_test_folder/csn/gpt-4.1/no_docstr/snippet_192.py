
class CONCATENATE_BASE_AND_KEY_Mechanism:

    def __init__(self, encKey):
        self.encKey = encKey

    def to_native(self):
        base = "BASE"
        return base + str(self.encKey)
