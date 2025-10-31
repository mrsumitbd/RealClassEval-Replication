class MINIDUMP_MEMORY_DESCRIPTOR:

    def __init__(self):
        self.StartOfMemoryRange = None
        self.MemoryLocation = None
        self.DataSize = None
        self.Rva = None

    def to_bytes(self):
        t = self.StartOfMemoryRange.to_bytes(4, byteorder='little', signed=False)
        t += self.MemoryLocation.to_bytes()
        return t

    @staticmethod
    def parse(buff):
        md = MINIDUMP_MEMORY_DESCRIPTOR()
        md.StartOfMemoryRange = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        md.MemoryLocation = MINIDUMP_LOCATION_DESCRIPTOR.parse(buff)
        md.DataSize = md.MemoryLocation.DataSize
        md.Rva = md.MemoryLocation.Rva
        return md

    def __str__(self):
        t = 'Start: %s' % hex(self.StartOfMemoryRange)
        t += 'Size: %s' % self.DataSize
        t += 'Rva: %s' % self.Rva
        return t