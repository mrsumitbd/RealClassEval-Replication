
class EXTRACT_KEY_FROM_KEY_Mechanism:

    def __init__(self, extractParams):
        self.extractParams = extractParams

    def to_native(self):
        return {'extractParams': self.extractParams}
