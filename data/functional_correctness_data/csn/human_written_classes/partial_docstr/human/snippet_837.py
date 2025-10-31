class TermsVersionConverter:
    """
    Registers Django URL path converter for Terms Version Numbers
    """
    regex = '[0-9.]+'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value