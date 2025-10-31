class Sampleable:
    """Element who can provide samples
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.sample = None

    def get_sample(self):
        """Return the a sample for the element
        """
        if self.sample is None:
            return self.get_default_sample()
        return self.sample

    def get_default_sample(self):
        """Return default value for the element
        """
        return 'my_%s' % self.name