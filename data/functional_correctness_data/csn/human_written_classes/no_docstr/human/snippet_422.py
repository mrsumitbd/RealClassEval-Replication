class DataType:

    def __init__(self, matched_type_codes):
        self._matched_type_codes = matched_type_codes

    def __eq__(self, other):
        return other in self._matched_type_codes

    def __ne__(self, other):
        return not self == other