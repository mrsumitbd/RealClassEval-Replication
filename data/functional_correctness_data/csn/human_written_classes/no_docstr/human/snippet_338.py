class ElapsedTime:

    def __init__(self, msg):
        self.msg = msg

    def __enter__(self):
        write('%-40s: ' % self.msg)
        self.start = clock()

    def __exit__(self, a1, a2, a3):
        self.stop = clock()
        writeln('%0.3f s' % self.get_time())

    def get_time(self):
        return self.stop - self.start