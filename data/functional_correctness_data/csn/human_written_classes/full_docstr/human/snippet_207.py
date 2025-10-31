class IJavaStreamParser:
    """
    API of the Java stream parser
    """

    def run(self):
        """
        Parses the input stream
        """
        raise NotImplementedError

    def dump(self, content):
        """
        Dumps to a string the given objects
        """
        raise NotImplementedError

    def _read_content(self, type_code, block_data, class_desc=None):
        """
        Parses the next content. Use with care (use only in a transformer)
        """