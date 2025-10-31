
class CodePageManager:

    def __init__(self, data):
        self.data = data

    @staticmethod
    def get_encoding_name(encoding):
        try:
            return encoding.name
        except AttributeError:
            return str(encoding)

    def get_encoding_name(self, encoding):
        return self.get_encoding_name(encoding)
