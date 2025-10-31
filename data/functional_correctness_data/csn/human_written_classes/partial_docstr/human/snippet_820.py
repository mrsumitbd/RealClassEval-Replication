class GenericFile:
    """
    Simple class for any file. Has same path lookup as netCDF4.Dataset.
    """

    def __init__(self, fpath):
        self.fpath = fpath

    def filepath(self):
        return self.fpath