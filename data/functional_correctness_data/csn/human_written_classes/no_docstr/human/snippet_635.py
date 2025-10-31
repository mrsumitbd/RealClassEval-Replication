from bx.align import Alignment, Component, src_split

class Writer:

    def __init__(self, file, attributes=None):
        if attributes is None:
            attributes = {}
        self.file = file
        self.block = 0
        self.src_split = True
        if 'src_split' in attributes:
            self.src_split = attributes['src_split']

    def write(self, alignment):
        if len(alignment.components) != 2:
            raise ValueError(f'{len(alignment.components)}-component alignment is not compatible with axt')
        c1 = alignment.components[0]
        c2 = alignment.components[1]
        if c1.strand != '+':
            c1 = c1.reverse_complement()
            c2 = c2.reverse_complement()
        if self.src_split:
            spec1, chr1 = src_split(c1.src)
            spec2, chr2 = src_split(c2.src)
        else:
            chr1, chr2 = (c1.src, c2.src)
        self.file.write(f'{self.block} {chr1} {c1.start + 1} {c1.start + c1.size} {chr2} {c2.start + 1} {c2.start + c2.size} {c2.strand} {alignment.score}\n')
        self.file.write(f'{c1.text}\n')
        self.file.write(f'{c2.text}\n')
        self.file.write('\n')
        self.block += 1

    def close(self):
        self.file.close()