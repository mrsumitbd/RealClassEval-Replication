class Writer:

    def __init__(self, file, attributes=None):
        if attributes is None:
            attributes = {}
        self.file = file
        if 'version' not in attributes:
            attributes['version'] = 1
        self.file.write('##maf version={}'.format(attributes['version']))
        for key in attributes:
            if key == 'version':
                continue
            self.file.writelines(f' {key}={attributes[key]}')
        self.file.write('\n')

    def write(self, alignment):
        self.file.write('a score=' + str(alignment.score))
        for key in alignment.attributes:
            self.file.write(f' {key}={alignment.attributes[key]}')
        self.file.write('\n')
        rows = []
        for c in alignment.components:
            if c.empty:
                rows.append(('e', c.src, str(c.start), str(c.size), c.strand, str(c.src_size), c.synteny_empty))
                continue
            rows.append(('s', c.src, str(c.start), str(c.size), c.strand, str(c.src_size), c.text))
            if c.quality is not None:
                rows.append(('q', c.src, '', '', '', '', c.quality))
            if c.synteny_left and c.synteny_right:
                rows.append(('i', c.src, '', '', '', '', ' '.join(map(str, c.synteny_left + c.synteny_right))))
        self.file.write(format_tabular(rows, 'llrrrrl'))
        self.file.write('\n')

    def close(self):
        self.file.close()