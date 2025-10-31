class MultiIndexed:
    """Similar to 'indexed' but wraps more than one axt_file"""

    def __init__(self, axt_filenames, keep_open=False):
        self.indexes = [Indexed(axt_file, axt_file + '.index') for axt_file in axt_filenames]

    def get(self, src, start, end):
        blocks = []
        for index in self.indexes:
            blocks += index.get(src, start, end)
        return blocks