class Matcher:
    """
    Appender matcher.
    @ivar cls: A class object.
    @type cls: I{classobj}
    """

    def __init__(self, cls):
        """
        @param cls: A class object.
        @type cls: I{classobj}
        """
        self.cls = cls

    def __eq__(self, x):
        if self.cls is None:
            return x is None
        else:
            return isinstance(x, self.cls)