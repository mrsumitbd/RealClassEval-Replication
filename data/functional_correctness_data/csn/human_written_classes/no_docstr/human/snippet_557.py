class MINIDUMP_THREAD_LIST:

    def __init__(self):
        self.NumberOfThreads = None
        self.Threads = []

    def to_bytes(self):
        t = len(self.Threads).to_bytes(4, byteorder='little', signed=False)
        for th in self.Threads:
            t += th.to_bytes()
        return t

    @staticmethod
    def parse(buff):
        mtl = MINIDUMP_THREAD_LIST()
        mtl.NumberOfThreads = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        for _ in range(mtl.NumberOfThreads):
            mtl.Threads.append(MINIDUMP_THREAD.parse(buff))
        return mtl