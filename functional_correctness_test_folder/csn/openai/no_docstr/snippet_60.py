
import codecs


class CodePageManager:
    def __init__(self, data):
        """
        Initialize the manager with a mapping of encoding identifiers to
        canonical encoding names. The mapping can be any mapping type
        (dict, list of tuples, etc.). If no data is provided, an empty
        dictionary is used.
        """
        self.data = dict(data) if data is not None else {}

    @staticmethod
    def get_encoding_name(encoding):
        """
        Return the canonical name for the given encoding using the
        standard codecs module. If the encoding is unknown, return None.
        """
        try:
            return codecs.lookup(encoding).name
        except LookupError:
            return None

    def get_encoding_name(self, encoding):
        """
        Return the canonical name for the given encoding. First look up
        the encoding in the instance's data mapping; if not found, fall
        back to the static method which uses the codecs module.
        """
        if encoding in self.data:
            return self.data[encoding]
        return self.__class__.get_encoding_name(encoding)
