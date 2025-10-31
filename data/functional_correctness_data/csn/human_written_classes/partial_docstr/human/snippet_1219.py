import os

class FASTQFile:
    """
    Base class for processing paired FASTQ filenames.

    Parameters
    ----------
    file : str
        Path to a FASTQ file.

    """

    def __init__(self, file: str):
        self.file = file
        self.path = os.path.abspath(file)
        self.basename = os.path.basename(self.path)
        self.dir = os.path.dirname(self.path)
        self.filename = self.basename.rstrip('.gz').rstrip('.fastq').rstrip('.fq')

    def __eq__(self, other):
        return self.name == other.name