class _LanguageSpecificStemmer:
    """
    This helper subclass offers the possibility
    to invoke a specific stemmer directly.
    This is useful if you already know the language to be stemmed at runtime.

    Create an instance of the Snowball stemmer.
    """

    def __init__(self):
        language = type(self).__name__.lower()
        if language.endswith('stemmer'):
            language = language[:-7]

    def __repr__(self):
        """
        Print out the string representation of the respective class.

        """
        return '<%s>' % type(self).__name__