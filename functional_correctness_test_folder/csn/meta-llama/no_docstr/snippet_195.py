
class KEY_DERIVATION_STRING_DATA_MechanismBase:
    def __init__(self, data, mechType):
        self.data = data
        self.mechType = mechType

    def to_native(self):
        return {
            'mechanism': self.mechType,
            'parameter': self.data
        }
