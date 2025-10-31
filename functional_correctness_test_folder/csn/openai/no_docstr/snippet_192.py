class CONCATENATE_BASE_AND_KEY_Mechanism:
    def __init__(self, encKey):
        self.encKey = encKey

    def to_native(self):
        if isinstance(self.encKey, bytes):
            key_str = self.encKey.decode('utf-8', errors='ignore')
        else:
            key_str = str(self.encKey)
        return "BASE" + key_str
