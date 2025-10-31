class Heart:
    """A Heart.

    Each beat touches a file.
    """

    def __init__(self, path):
        self.path = path

    def getFile(self):
        """Get the file being touched"""
        return self.path

    def beat(self):
        """Touch the file"""
        self.path.touch()