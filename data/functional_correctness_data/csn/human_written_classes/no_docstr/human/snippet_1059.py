from lhc.entities import GenomicInterval
import pysam

class TabixFileWrapper:

    def __init__(self, filename: str):
        self.index = pysam.TabixFile(filename)

    def __getitem__(self, item: GenomicInterval):
        return self.index.fetch(item.chromosome, item.start.position, item.stop.position)