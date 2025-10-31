class FusingAlignmentWriter:
    """
    Wrapper for an alignment Writer which attempts to fuse adjacent blocks
    """

    def __init__(self, maf_writer):
        self.maf_writer = maf_writer
        self.last = None

    def write(self, m):
        if not self.last:
            self.last = m
        else:
            fused = fuse(self.last, m)
            if fused:
                self.last = fused
            else:
                self.maf_writer.write(self.last)
                self.last = m

    def close(self):
        if self.last:
            self.maf_writer.write(self.last)
        self.maf_writer.close()