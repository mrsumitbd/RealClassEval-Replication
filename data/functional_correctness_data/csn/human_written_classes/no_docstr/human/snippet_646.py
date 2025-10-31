import struct

class QdnaWriter:

    def __init__(self, file):
        self.file = file

    def write(self, seq):
        text = seq.text
        if text is None:
            text = ''
        version = 512
        headerLen = 20
        offset = headerLen + 8
        nameOffset = 0
        if seq.name is not None and seq.name != '':
            nameOffset = 28
            offset += len(seq.name) + 1
            name = seq.name + chr(0)
        dataOffset = offset
        offset += len(text)
        assert seq.codebook is None, 'QdnaWriter.write() does not support codebooks yet'
        propOffset = 0
        self.file.write(struct.pack(f'{seq.byte_order}L', qdnaMagic))
        self.file.write(struct.pack(f'{seq.byte_order}L', version))
        self.file.write(struct.pack(f'{seq.byte_order}L', headerLen))
        self.file.write(struct.pack(f'{seq.byte_order}L', dataOffset))
        self.file.write(struct.pack(f'{seq.byte_order}L', nameOffset))
        self.file.write(struct.pack(f'{seq.byte_order}L', len(text)))
        self.file.write(struct.pack(f'{seq.byte_order}L', propOffset))
        if nameOffset != 0:
            self.file.write(name)
        self.file.write(text)

    def close(self):
        self.file.close()