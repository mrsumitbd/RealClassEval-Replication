class MINIDUMP_THREAD_EX_LIST:

    def __init__(self):
        self.NumberOfThreads = None
        self.Threads = []

    @staticmethod
    def parse(buff):
        mtel = MINIDUMP_THREAD_EX_LIST()
        mtel.NumberOfThreads = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        for _ in range(mtel.NumberOfThreads):
            mtel.Threads.append(MINIDUMP_THREAD_EX.parse(buff))
        return mtel