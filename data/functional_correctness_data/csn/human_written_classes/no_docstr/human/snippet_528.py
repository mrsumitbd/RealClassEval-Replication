class BenchRes:

    def __init__(self, name, time_ms, mem_mb):
        self.name = name
        self.time_ms = time_ms
        self.mem_mb = mem_mb

    def __repr__(self):
        return '%s\t%0.2f\t%0.2f' % (self.name, self.time_ms, self.mem_mb)

    def str_res(self):
        return '%0.2f\t%0.2f' % (self.time_ms, self.mem_mb)