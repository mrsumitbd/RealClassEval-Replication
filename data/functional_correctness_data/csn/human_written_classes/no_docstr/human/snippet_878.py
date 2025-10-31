class Hash:

    def __init__(self, name, data, magic):
        for size, poly in SIZES:
            if size > len(data):
                poly = size + poly
                break
        else:
            raise AssertionError('ran out of polynomials')
        print(size, 'slots in hash table')
        table = [None] * size
        mask = size - 1
        n = 0
        hash = myhash
        for key, value in data:
            h = hash(key, magic)
            i = ~h & mask
            v = table[i]
            if v is None:
                table[i] = value
                continue
            incr = (h ^ h >> 3) & mask
            if not incr:
                incr = mask
            while 1:
                n = n + 1
                i = i + incr & mask
                v = table[i]
                if v is None:
                    table[i] = value
                    break
                incr = incr << 1
                if incr > mask:
                    incr = incr ^ poly
        print(n, 'collisions')
        self.collisions = n
        for i in range(len(table)):
            if table[i] is None:
                table[i] = 0
        self.data = Array(name + '_hash', table)
        self.magic = magic
        self.name = name
        self.size = size
        self.poly = poly

    def dump(self, file, trace):
        self.data.dump(file, trace)
        file.write('#define %s_magic %d\n' % (self.name, self.magic))
        file.write('#define %s_size %d\n' % (self.name, self.size))
        file.write('#define %s_poly %d\n' % (self.name, self.poly))